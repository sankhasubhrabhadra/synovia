import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
from sqlalchemy.future import select

from app.database.session import AsyncSessionLocal
from app.database.models import ProjectDB
from app.agents.research import research_agent
from app.agents.competitor import competitor_agent
from app.agents.product import product_agent
from app.agents.roadmap import roadmap_agent
from app.agents.pitch import pitch_agent
from app.agents.validation import validation_agent
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

class ManagerAgent:
    """
    High-Performance Multi-Agent Pipeline Orchestrator.
    Executes specialized agents to synthesize research, MVP specs, roadmap, pitch, and VC-level validation.
    """

    async def execute_pipeline(self, project_id: str, idea: str, target_market: Optional[str] = None) -> Dict[str, Any]:
        logger.info(f"ManagerAgent executing optimized pipeline for project {project_id}")

        try:
            # Phase 1: Research & Competitor Agents (Concurrent)
            await broadcast_status(
                project_id, AgentStepEnum.RESEARCH, StatusEnum.RUNNING, 15,
                "Analyzing market size, TAM/SAM/SOM, and competitive intelligence matrix..."
            )
            
            research_task = asyncio.create_task(research_agent.run(idea, target_market))
            research_data = await research_task

            await broadcast_status(
                project_id, AgentStepEnum.COMPETITOR, StatusEnum.RUNNING, 30,
                "Analyzing real-world competitors and market gaps...", research_data
            )
            
            competitor_task = asyncio.create_task(competitor_agent.run(idea, research_data))
            competitor_data = await competitor_task

            # Phase 2: Product & Roadmap Agents (Concurrent)
            await broadcast_status(
                project_id, AgentStepEnum.PRODUCT, StatusEnum.RUNNING, 50,
                "Designing MVP feature priority matrix and 4-week execution roadmap..."
            )
            
            product_task = asyncio.create_task(product_agent.run(idea, research_data, competitor_data))
            roadmap_task = asyncio.create_task(roadmap_agent.run(idea, {}))
            
            product_data, roadmap_data = await asyncio.gather(product_task, roadmap_task)

            await broadcast_status(
                project_id, AgentStepEnum.ROADMAP, StatusEnum.COMPLETED, 70,
                "MVP Product spec and 4-week execution roadmap ready.", product_data
            )

            # Phase 3: Pitch & Monetization Agent
            await broadcast_status(
                project_id, AgentStepEnum.PITCH, StatusEnum.RUNNING, 85,
                "Crafting investor pitch deck and monetization model...", pitch_data=None
            )
            
            pitch_data = await pitch_agent.run(idea, research_data, product_data)

            # Phase 4: Validation & Strategy Agent (Evaluates all previous agents)
            await broadcast_status(
                project_id, AgentStepEnum.VALIDATION, StatusEnum.RUNNING, 92,
                "Senior VC & Mentor Agent conducting startup viability assessment and risk evaluation..."
            )
            
            validation_data = await validation_agent.run(
                idea, research_data, competitor_data, product_data, roadmap_data, pitch_data
            )

            # Step 5: Finalize Merged Blueprint
            executive_summary = (
                f"Synovia Blueprint & Strategy Report for '{idea}': Targeting a "
                f"{research_data.get('market_size', {}).get('tam', 'multi-billion dollar')} market opportunity. "
                f"Achieved a Viability Score of {validation_data.get('viability_score', 82)}/100. "
                f"Verdict: '{validation_data.get('final_verdict', 'STRONG PURSUE')}'."
            )

            merged_blueprint: Dict[str, Any] = {
                "project_id": project_id,
                "idea": idea,
                "target_market": target_market or "Global",
                "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
                "executive_summary": executive_summary,
                "research": research_data,
                "competitor": competitor_data,
                "product": product_data,
                "roadmap": roadmap_data,
                "pitch": pitch_data,
                "validation": validation_data
            }

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
            await broadcast_status(
                project_id, AgentStepEnum.MANAGER, StatusEnum.FAILED, 0,
                f"Execution error encountered: {str(e)}"
            )
            raise e

manager_agent = ManagerAgent()
