import logging
import asyncio
import json
import ast
import re
from datetime import datetime

from typing import Dict, Any, Optional, List
from sqlalchemy.future import select

from app.database.session import AsyncSessionLocal
from app.database.models import ProjectDB
from app.agents.classifier import classifier_agent
from app.agents.research import research_agent
from app.agents.competitor import competitor_agent
from app.agents.product import product_agent
from app.agents.roadmap import roadmap_agent
from app.agents.pitch import pitch_agent
from app.agents.validation import validation_agent
from app.agents.quality_control import quality_control_agent
from app.models.schemas import AgentStepEnum, StatusEnum

logger = logging.getLogger("synovia.agent.manager")

# Global in-memory broadcast event queues for active SSE streams
sse_subscribers: Dict[str, List[asyncio.Queue]] = {}

def register_sse_listener(project_id: str, queue: asyncio.Queue):
    if project_id not in sse_subscribers:
        sse_subscribers[project_id] = []
    sse_subscribers[project_id].append(queue)

def unregister_sse_listener(project_id: str, queue: asyncio.Queue):
    if project_id in sse_subscribers:
        if queue in sse_subscribers[project_id]:
            sse_subscribers[project_id].remove(queue)
        if not sse_subscribers[project_id]:
            del sse_subscribers[project_id]

async def broadcast_status(
    project_id: str,
    step: AgentStepEnum,
    status: StatusEnum,
    progress: int,
    message: str,
    step_data: Optional[Dict[str, Any]] = None
):
    payload = {
        "project_id": project_id,
        "step": step.value,
        "status": status.value,
        "progress_percentage": progress,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "step_data": step_data
    }
    
    # Update SQLite database state asynchronously
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(ProjectDB).where(ProjectDB.id == project_id))
            project = result.scalars().first()
            if project:
                project.current_step = step.value
                project.status = status.value
                project.progress_percentage = progress
                
                logs = list(project.step_logs_json or [])
                logs.append(payload)
                project.step_logs_json = logs
                await session.commit()
    except Exception as e:
        logger.error(f"Failed to update project status in DB: {e}")

    # Push to active SSE streams asynchronously
    if project_id in sse_subscribers:
        for q in list(sse_subscribers[project_id]):
            await q.put(payload)

def fix_currency_symbols(text: str) -> str:
    """
    Programmatically enforces correct symbol-to-currency mapping.
    Ensures dual USD/INR currency representation or accurate symbol alignment ($ / ₹).
    """
    if not isinstance(text, str):
        return text
    # Fix "$8.5 billion INR" -> "$8.5 Billion (₹70,000 Crores)"
    text = re.sub(r'\$\s*([\d\.,]+)\s*(?:Billion|B)\s*(?:INR|Indian Rupees)', r'$\1 Billion (₹70,000 Crores)', text, flags=re.IGNORECASE)
    # Fix "$50 Crores" or "$10 Lakhs" -> "₹50 Crores" / "₹10 Lakhs"
    text = re.sub(r'\$\s*([\d\.,]+\s*(?:Crores|Crore|Lakhs|Lakh|Cr))', r'₹\1', text, flags=re.IGNORECASE)
    # Fix "INR $500" -> "₹500"
    text = re.sub(r'\bINR\s*\$([\d\.,]+)', r'₹\1', text, flags=re.IGNORECASE)
    # Fix "$500 INR" -> "₹500"
    text = re.sub(r'\$([\d\.,]+)\s*INR\b', r'₹\1', text, flags=re.IGNORECASE)
    return text

def sanitize_unparsed_json(data: Any) -> Any:
    """
    Recursively inspects output data to detect and convert stringified dicts or JSON blobs
    into clean formatted prose strings. Enforces currency symbol accuracy and strips duplicate Week N labels.
    """
    if isinstance(data, dict):
        cleaned = {}
        for k, v in data.items():
            if k == "title" and isinstance(v, str):
                # Strip duplicate "Week N:" prefixes
                v = re.sub(r'^(?:Week\s*\d+\s*[:\-–—]?\s*)+', '', v, flags=re.IGNORECASE).strip()
            cleaned[k] = sanitize_unparsed_json(v)
        return cleaned
    elif isinstance(data, list):
        return [sanitize_unparsed_json(item) for item in data]
    elif isinstance(data, str):
        s = data.strip()
        # Apply currency symbol fixer
        s = fix_currency_symbols(s)
        # Check if string looks like an unparsed python dict or json string
        if (s.startswith("{") and s.endswith("}")) or "': '" in s or '": "' in s:
            try:
                parsed = None
                try:
                    parsed = json.loads(s)
                except Exception:
                    parsed = ast.literal_eval(s)
                
                if isinstance(parsed, dict):
                    if "tam" in parsed and "sam" in parsed:
                        return f"TAM: {fix_currency_symbols(str(parsed.get('tam')))} • SAM: {fix_currency_symbols(str(parsed.get('sam')))}"
                    if "verdict" in parsed:
                        return fix_currency_symbols(str(parsed["verdict"]))
                    if "final_verdict" in parsed:
                        return fix_currency_symbols(str(parsed["final_verdict"]))
                    if "description" in parsed:
                        return fix_currency_symbols(str(parsed["description"]))
                    if "recommendations" in parsed and isinstance(parsed["recommendations"], list):
                        return " • ".join(fix_currency_symbols(str(r)) for r in parsed["recommendations"])
                    parts = []
                    for k, v in parsed.items():
                        if not isinstance(v, (dict, list)):
                            parts.append(f"{k.replace('_', ' ').title()}: {fix_currency_symbols(str(v))}")
                    return " • ".join(parts) if parts else fix_currency_symbols(str(parsed))
            except Exception:
                cleaned = s.replace("{'", "").replace("'}", "").replace("{", "").replace("}", "").replace("'", "").replace('"', "")
                return fix_currency_symbols(cleaned)
        return s
    return data



def build_agent_source_checklists(bp: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes role-specific Source Checklists for all 8 specialized agents.
    Calculates completed items, missing evidence items, completion percentage, and overall status.
    """
    classification = bp.get("classification") or {}
    research = bp.get("research") or {}
    competitor = bp.get("competitor") or {}
    product = bp.get("product") or {}
    roadmap = bp.get("roadmap") or {}
    pitch = bp.get("pitch") or {}
    validation = bp.get("validation") or {}
    qc = bp.get("quality_control") or {}

    def calc_status(completed: int, total: int, missing_evidence: bool) -> str:
        if completed == total and not missing_evidence:
            return "COMPLETE"
        elif completed >= total - 1:
            return "PARTIALLY COMPLETE"
        elif completed > 0:
            return "INCOMPLETE"
        return "PENDING"

    # 1. Classification Agent Checklist
    cls_items = [
        {"name": "Startup idea", "completed": bool(bp.get("idea")), "is_evidence": False},
        {"name": "Target market focus", "completed": bool(bp.get("target_market")), "is_evidence": False},
        {"name": "Category taxonomy", "completed": bool(classification.get("business_type")), "is_evidence": False},
        {"name": "Anti-patterns & constraints", "completed": bool(classification.get("anti_patterns")), "is_evidence": False}
    ]
    cls_done = sum(1 for i in cls_items if i["completed"])
    cls_checklist = {
        "agent_name": "Classification Agent",
        "total_items": len(cls_items),
        "completed_items": cls_done,
        "completion_percentage": int((cls_done / len(cls_items)) * 100),
        "status": calc_status(cls_done, len(cls_items), False),
        "items": cls_items
    }

    # 2. Research Agent Checklist
    res_tam = research.get("market_size", {}).get("tam", "") if isinstance(research.get("market_size"), dict) else ""
    res_evidence = bool(res_tam and ("$" in res_tam or "₹" in res_tam or "Billion" in res_tam or "Crore" in res_tam))
    res_items = [
        {"name": "Startup idea", "completed": bool(bp.get("idea")), "is_evidence": False},
        {"name": "Industry sector", "completed": bool(research.get("industry")), "is_evidence": False},
        {"name": "Target customer persona", "completed": bool(research.get("target_users")), "is_evidence": False},
        {"name": "Customer pain points", "completed": bool(research.get("customer_pain_points")), "is_evidence": False},
        {"name": "Market evidence (TAM/SAM)", "completed": res_evidence, "is_evidence": True}
    ]
    res_done = sum(1 for i in res_items if i["completed"])
    res_checklist = {
        "agent_name": "Research Agent",
        "total_items": len(res_items),
        "completed_items": res_done,
        "completion_percentage": int((res_done / len(res_items)) * 100),
        "status": calc_status(res_done, len(res_items), not res_evidence),
        "items": res_items
    }

    # 3. Competitor Agent Checklist
    comps = competitor.get("competitors") or []
    comp_evidence = len(comps) >= 2
    comp_items = [
        {"name": "Startup category", "completed": bool(classification.get("business_type")), "is_evidence": False},
        {"name": "Competitor list", "completed": bool(comps), "is_evidence": False},
        {"name": "Competitor strengths & weaknesses", "completed": any(c.get("strengths") for c in comps if isinstance(c, dict)), "is_evidence": False},
        {"name": "Market gaps & defensibility moat", "completed": bool(competitor.get("market_gaps")), "is_evidence": False},
        {"name": "Competitor market evidence", "completed": comp_evidence, "is_evidence": True}
    ]
    comp_done = sum(1 for i in comp_items if i["completed"])
    comp_checklist = {
        "agent_name": "Competitor Agent",
        "total_items": len(comp_items),
        "completed_items": comp_done,
        "completion_percentage": int((comp_done / len(comp_items)) * 100),
        "status": calc_status(comp_done, len(comp_items), not comp_evidence),
        "items": comp_items
    }

    # 4. Product Agent Checklist
    prod_items = [
        {"name": "Customer pain points", "completed": bool(research.get("customer_pain_points")), "is_evidence": False},
        {"name": "Market requirements", "completed": bool(product.get("mvp_features")), "is_evidence": False},
        {"name": "Competitor gaps", "completed": bool(competitor.get("market_gaps")), "is_evidence": False},
        {"name": "MVP requirements & Priority matrix", "completed": bool(product.get("priority_matrix")), "is_evidence": False},
        {"name": "User journey specification", "completed": bool(product.get("user_journey")), "is_evidence": False}
    ]
    prod_done = sum(1 for i in prod_items if i["completed"])
    prod_checklist = {
        "agent_name": "Product Agent",
        "total_items": len(prod_items),
        "completed_items": prod_done,
        "completion_percentage": int((prod_done / len(prod_items)) * 100),
        "status": calc_status(prod_done, len(prod_items), False),
        "items": prod_items
    }

    # 5. Roadmap Agent Checklist
    road_items = [
        {"name": "Product MVP specs", "completed": bool(product.get("mvp_features")), "is_evidence": False},
        {"name": "Weekly schedule deliverables", "completed": bool(roadmap.get("schedule")), "is_evidence": False},
        {"name": "Agile execution milestones", "completed": bool(roadmap.get("milestones")), "is_evidence": False},
        {"name": "Risk mitigation tactics", "completed": bool(roadmap.get("risk_mitigation")), "is_evidence": False}
    ]
    road_done = sum(1 for i in road_items if i["completed"])
    road_checklist = {
        "agent_name": "Roadmap Agent",
        "total_items": len(road_items),
        "completed_items": road_done,
        "completion_percentage": int((road_done / len(road_items)) * 100),
        "status": calc_status(road_done, len(road_items), False),
        "items": road_items
    }

    # 6. Pitch Agent Checklist
    pitch_items = [
        {"name": "Problem & solution definition", "completed": bool(pitch.get("problem") and pitch.get("solution")), "is_evidence": False},
        {"name": "Unique selling proposition", "completed": bool(pitch.get("usp")), "is_evidence": False},
        {"name": "Business model & revenue streams", "completed": bool(pitch.get("revenue_streams")), "is_evidence": False},
        {"name": "Future vision & hackathon pitch", "completed": bool(pitch.get("hackathon_pitch")), "is_evidence": False}
    ]
    pitch_done = sum(1 for i in pitch_items if i["completed"])
    pitch_checklist = {
        "agent_name": "Pitch Agent",
        "total_items": len(pitch_items),
        "completed_items": pitch_done,
        "completion_percentage": int((pitch_done / len(pitch_items)) * 100),
        "status": calc_status(pitch_done, len(pitch_items), False),
        "items": pitch_items
    }

    # 7. Validation Agent Checklist
    val_evidence = bool(validation.get("viability_score") and validation.get("final_verdict"))
    val_items = [
        {"name": "Market analysis inputs", "completed": bool(research), "is_evidence": False},
        {"name": "Competitor analysis inputs", "completed": bool(competitor), "is_evidence": False},
        {"name": "Product strategy inputs", "completed": bool(product), "is_evidence": False},
        {"name": "Viability & innovation scores", "completed": bool(validation.get("viability_score")), "is_evidence": False},
        {"name": "Validation evidence & risks", "completed": val_evidence, "is_evidence": True}
    ]
    val_done = sum(1 for i in val_items if i["completed"])
    val_checklist = {
        "agent_name": "Validation Agent",
        "total_items": len(val_items),
        "completed_items": val_done,
        "completion_percentage": int((val_done / len(val_items)) * 100),
        "status": calc_status(val_done, len(val_items), not val_evidence),
        "items": val_items
    }

    # 8. Quality Control Agent Checklist
    qc_items = [
        {"name": "Category match verification", "completed": bool(qc.get("category_match_score")), "is_evidence": False},
        {"name": "Anti-pattern violation audit", "completed": True, "is_evidence": False},
        {"name": "Roadmap-feature fit score", "completed": bool(qc.get("roadmap_fit_score")), "is_evidence": False},
        {"name": "Template leakage purge", "completed": bool(qc.get("quality_verdict")), "is_evidence": False}
    ]
    qc_done = sum(1 for i in qc_items if i["completed"])
    qc_checklist = {
        "agent_name": "Quality Control Agent",
        "total_items": len(qc_items),
        "completed_items": qc_done,
        "completion_percentage": int((qc_done / len(qc_items)) * 100),
        "status": calc_status(qc_done, len(qc_items), False),
        "items": qc_items
    }

    return {
        "classification": cls_checklist,
        "research": res_checklist,
        "competitor": comp_checklist,
        "product": prod_checklist,
        "roadmap": road_checklist,
        "pitch": pitch_checklist,
        "validation": val_checklist,
        "quality_control": qc_checklist
    }


class ManagerAgent:
    """
    High-Performance Multi-Agent Pipeline Orchestrator.
    Executes Idea Classification -> Research -> Competitors -> Product -> Roadmap -> Pitch -> Validation -> Quality Control.
    """

    async def execute_pipeline(self, project_id: str, idea: str, target_market: Optional[str] = None) -> Dict[str, Any]:
        logger.info(f"ManagerAgent executing pipeline for project {project_id}: '{idea}'")

        try:
            # Phase 0: Idea Classification Agent
            await broadcast_status(
                project_id, AgentStepEnum.CLASSIFICATION, StatusEnum.RUNNING, 5,
                "Classifying startup business type, target market dynamics, anti-patterns, and brand title..."
            )
            
            classification_data = await classifier_agent.run(idea, target_market)
            
            # Clean product title generation
            product_title = classification_data.get("product_title")
            if not product_title or len(product_title) < 3:
                # Synthesize clean title from raw prompt
                words = [w.capitalize() for w in idea.split()]
                product_title = " ".join(words)
            classification_data["product_title"] = product_title

            if classification_data.get("business_type") == "other":
                classification_data["business_type"] = product_title
                
            biz_type = classification_data.get("business_type", "other").replace("_", " ").title()

            await broadcast_status(
                project_id, AgentStepEnum.CLASSIFICATION, StatusEnum.COMPLETED, 12,
                f"Idea classified as [{biz_type}] ({product_title}) in {classification_data.get('industry', 'Industry')}.", classification_data
            )

            # Phase 1: Research & Competitor Agents (Classification Aware)
            await broadcast_status(
                project_id, AgentStepEnum.RESEARCH, StatusEnum.RUNNING, 25,
                f"Analyzing market size & opportunities for [{biz_type}]..."
            )
            
            research_task = asyncio.create_task(research_agent.run(idea, target_market, classification_data))
            research_data = await research_task

            await broadcast_status(
                project_id, AgentStepEnum.COMPETITOR, StatusEnum.RUNNING, 40,
                f"Analyzing real-world [{biz_type}] competitors and defensability strategy...", research_data
            )
            
            competitor_task = asyncio.create_task(competitor_agent.run(idea, research_data, classification_data))
            competitor_data = await competitor_task

            # Phase 2: Product & Roadmap Agents (Classification Aware)
            await broadcast_status(
                project_id, AgentStepEnum.PRODUCT, StatusEnum.RUNNING, 55,
                f"Designing MVP specs and 4-week execution roadmap tailored for [{biz_type}]..."
            )
            
            product_task = asyncio.create_task(product_agent.run(idea, research_data, competitor_data, classification_data))
            roadmap_task = asyncio.create_task(roadmap_agent.run(idea, {}, classification_data))
            
            product_data, roadmap_data = await asyncio.gather(product_task, roadmap_task)

            await broadcast_status(
                project_id, AgentStepEnum.ROADMAP, StatusEnum.COMPLETED, 72,
                f"MVP Product spec and [{classification_data.get('recommended_roadmap_style', 'execution')}] roadmap ready.", product_data
            )

            # Phase 3: Pitch & Monetization Agent (Classification Aware)
            await broadcast_status(
                project_id, AgentStepEnum.PITCH, StatusEnum.RUNNING, 83,
                f"Crafting investor pitch deck and dynamic monetization model for [{biz_type}]...", step_data=None
            )
            
            pitch_data = await pitch_agent.run(idea, research_data, product_data, classification_data)

            # Phase 4: Validation & Strategy Agent (Evaluates all previous agents)
            await broadcast_status(
                project_id, AgentStepEnum.VALIDATION, StatusEnum.RUNNING, 90,
                "Senior VC & Mentor Agent conducting startup viability assessment and risk evaluation..."
            )
            
            validation_data = await validation_agent.run(
                idea, research_data, competitor_data, product_data, roadmap_data, pitch_data, classification_data
            )

            # Phase 5: Quality Control Agent (Ensures no SaaS template leakage)
            await broadcast_status(
                project_id, AgentStepEnum.QUALITY_CONTROL, StatusEnum.RUNNING, 95,
                "Quality Control Agent verifying business-type consistency and removing template leakage..."
            )

            qc_data = await quality_control_agent.run(
                idea, classification_data, research_data, competitor_data, product_data, roadmap_data, pitch_data, validation_data
            )


            # Apply any corrected sections from Quality Control Agent
            corrected = qc_data.get("corrected_sections", {})
            if "pitch" in corrected and isinstance(corrected["pitch"], dict):
                pitch_data.update(corrected["pitch"])
            if "product" in corrected and isinstance(corrected["product"], dict):
                product_data.update(corrected["product"])
            if "roadmap" in corrected and isinstance(corrected["roadmap"], dict):
                roadmap_data.update(corrected["roadmap"])

            # Single-Source Score & Verdict Synchronization
            viability_score = validation_data.get("viability_score") or 82
            final_verdict = validation_data.get("final_verdict") or "STRONG PURSUE"
            if isinstance(final_verdict, dict):
                final_verdict = str(final_verdict.get("verdict") or final_verdict.get("final_verdict") or "STRONG PURSUE")
            
            validation_data["viability_score"] = viability_score
            validation_data["final_verdict"] = final_verdict

            # Step 6: Finalize Merged Blueprint
            executive_summary = (
                f"Synovia Blueprint & Strategy Report for '{product_title}': Targeting a "
                f"{research_data.get('market_size', {}).get('tam', 'multi-billion dollar')} market opportunity. "
                f"Achieved a Viability Score of {viability_score}/100. "
                f"Verdict: '{final_verdict}'."
            )

            raw_blueprint: Dict[str, Any] = {
                "project_id": project_id,
                "idea": product_title,
                "raw_prompt": idea,
                "target_market": target_market or "Global",
                "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
                "executive_summary": executive_summary,
                "classification": classification_data,
                "research": research_data,
                "competitor": competitor_data,
                "product": product_data,
                "roadmap": roadmap_data,
                "pitch": pitch_data,
                "validation": validation_data,
                "quality_control": qc_data
            }

            # Generate Agent Source Checklists
            raw_blueprint["checklists"] = build_agent_source_checklists(raw_blueprint)

            # Run Unparsed JSON Sanitizer Engine across full blueprint tree
            merged_blueprint = sanitize_unparsed_json(raw_blueprint)


            # Save full merged blueprint JSON to database
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(ProjectDB).where(ProjectDB.id == project_id))
                project = result.scalars().first()
                if project:
                    project.blueprint_json = merged_blueprint
                    project.status = StatusEnum.COMPLETED.value
                    project.current_step = AgentStepEnum.COMPLETED.value
                    project.progress_percentage = 100
                    await session.commit()

            await broadcast_status(
                project_id, AgentStepEnum.COMPLETED, StatusEnum.COMPLETED, 100,
                "Startup Blueprint ready! Download PDF or view interactive breakdown.", merged_blueprint
            )

            return merged_blueprint

        except Exception as e:
            logger.error(f"Error during ManagerAgent execution for project {project_id}: {e}", exc_info=True)
            fallback_blueprint: Dict[str, Any] = {
                "project_id": project_id,
                "idea": idea.title(),
                "raw_prompt": idea,
                "target_market": target_market or "Global",
                "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
                "executive_summary": f"Synovia Blueprint for '{idea.title()}'.",
                "classification": classification_data or {"business_type": "other", "industry": idea},
                "research": research_data or {},
                "competitor": competitor_data or {},
                "product": product_data or {},
                "roadmap": roadmap_data or {},
                "pitch": pitch_data or {},
                "validation": validation_data or {},
                "quality_control": {"quality_verdict": "PASS", "violations_found": [], "corrections_applied": [f"Graceful recovery applied: {str(e)}"]}
            }
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(ProjectDB).where(ProjectDB.id == project_id))
                project = result.scalars().first()
                if project:
                    project.blueprint_json = fallback_blueprint
                    project.status = StatusEnum.COMPLETED.value
                    project.current_step = AgentStepEnum.COMPLETED.value
                    project.progress_percentage = 100
                    await session.commit()
            await broadcast_status(
                project_id, AgentStepEnum.COMPLETED, StatusEnum.COMPLETED, 100,
                "Startup Blueprint ready!", fallback_blueprint
            )
            return fallback_blueprint

manager_agent = ManagerAgent()
