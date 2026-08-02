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
from app.agents.architect import architect_agent
from app.agents.roadmap import roadmap_agent
from app.agents.pitch import pitch_agent
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
    Manager Agent orchestrates all specialized AI agents asynchronously.
    Pipeline: Research -> Competitor -> Product -> Technical Architect -> Roadmap -> Pitch Deck -> Merge
    Returns one unified, merged JSON object containing the complete Startup Blueprint.
    """

    async def run_pipeline(self, idea: str, target_market: Optional[str] = None) -> Dict[str, Any]:
        """
        Pure async pipeline execution method. Orchestrates all agents and returns one merged JSON object.
        """
        logger.info(f"ManagerAgent orchestrating pipeline for startup idea: '{idea}'")
        
        # 1. Execute Market Research Agent
        research_data = await research_agent.run(idea=idea, target_market=target_market)
        
        # 2. Execute Competitor Intelligence Agent
        competitor_data = await competitor_agent.run(idea=idea, research_data=research_data)
        
        # 3. Execute Product Manager Agent
        product_data = await product_agent.run(idea=idea, research_data=research_data, competitor_data=competitor_data)
        
        # 4. Execute Technical Architect Agent
        architect_data = await architect_agent.run(idea=idea, product_data=product_data)
        
        # 5. Execute Concurrent / Sequential Downstream Agents (Roadmap & Pitch Deck)
        # Roadmap and Pitch can run concurrently once research, competitor, product, and architect contexts are ready!
        roadmap_task = asyncio.create_task(roadmap_agent.run(idea=idea, architect_data=architect_data))
        pitch_task = asyncio.create_task(pitch_agent.run(idea=idea, research_data=research_data, product_data=product_data))
        
        roadmap_data, pitch_data = await asyncio.gather(roadmap_task, pitch_task)

        # 6. Merge all agent outputs into ONE comprehensive, structured JSON blueprint
        executive_summary = (
            f"Synovia Blueprint for '{idea}': An innovative AI-native solution targeting a "
            f"{research_data.get('market_size', {}).get('tam', 'multi-billion dollar')} opportunity. "
            f"Built with {architect_data.get('frontend', {}).get('technology', 'Next.js 15')} and "
            f"{architect_data.get('backend', {}).get('technology', 'FastAPI')}, backed by a 4-week agile roadmap."
        )

        merged_blueprint: Dict[str, Any] = {
            "idea": idea,
            "target_market": target_market or "Global",
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            "executive_summary": executive_summary,
            "research": research_data,
            "competitor": competitor_data,
            "product": product_data,
            "architect": architect_data,
            "roadmap": roadmap_data,
            "pitch": pitch_data
        }

        return merged_blueprint

    async def execute_pipeline(self, project_id: str, idea: str, target_market: Optional[str] = None) -> Dict[str, Any]:
        """
        Orchestrates all agents asynchronously with live SSE status broadcasting and DB persistence.
        Returns the final merged JSON object.
        """
        logger.info(f"ManagerAgent starting full background pipeline execution for project {project_id}")

        try:
            # Step 1: Research Agent
            await broadcast_status(
                project_id, AgentStepEnum.RESEARCH, StatusEnum.RUNNING, 15,
                "Researching market size, industry trends, TAM/SAM/SOM, and target customer pain points..."
            )
            research_data = await research_agent.run(idea, target_market)
            await broadcast_status(
                project_id, AgentStepEnum.RESEARCH, StatusEnum.COMPLETED, 30,
                "Market research completed successfully.", research_data
            )

            # Step 2: Competitor Agent
            await broadcast_status(
                project_id, AgentStepEnum.COMPETITOR, StatusEnum.RUNNING, 35,
                "Finding competitors, analyzing market strengths, weaknesses, and defensibility gaps..."
            )
            competitor_data = await competitor_agent.run(idea, research_data)
            await broadcast_status(
                project_id, AgentStepEnum.COMPETITOR, StatusEnum.COMPLETED, 48,
                "Competitor intelligence matrix generated.", competitor_data
            )

            # Step 3: Product Agent
            await broadcast_status(
                project_id, AgentStepEnum.PRODUCT, StatusEnum.RUNNING, 52,
                "Designing MVP core features, user journey, and feature priority matrix..."
            )
            product_data = await product_agent.run(idea, research_data, competitor_data)
            await broadcast_status(
                project_id, AgentStepEnum.PRODUCT, StatusEnum.COMPLETED, 65,
                "Product feature specification ready.", product_data
            )

            # Step 4: Technical Architect Agent
            await broadcast_status(
                project_id, AgentStepEnum.ARCHITECT, StatusEnum.RUNNING, 70,
                "Generating production technical architecture, backend stack, DB schema, and project structure..."
            )
            architect_data = await architect_agent.run(idea, product_data)
            await broadcast_status(
                project_id, AgentStepEnum.ARCHITECT, StatusEnum.COMPLETED, 80,
                "Technical system architecture design complete.", architect_data
            )

            # Step 5 & 6: Roadmap & Pitch Deck Agents (Executed concurrently with asyncio.gather)
            await broadcast_status(
                project_id, AgentStepEnum.ROADMAP, StatusEnum.RUNNING, 85,
                "Building 4-week agile execution roadmap and preparing investor pitch deck..."
            )
            
            roadmap_task = asyncio.create_task(roadmap_agent.run(idea, architect_data))
            pitch_task = asyncio.create_task(pitch_agent.run(idea, research_data, product_data))
            
            roadmap_data, pitch_data = await asyncio.gather(roadmap_task, pitch_task)

            await broadcast_status(
                project_id, AgentStepEnum.ROADMAP, StatusEnum.COMPLETED, 92,
                "Execution roadmap finalized.", roadmap_data
            )
            await broadcast_status(
                project_id, AgentStepEnum.PITCH, StatusEnum.COMPLETED, 96,
                "Investor pitch deck generated.", pitch_data
            )

            # Step 7: Merge & Finalize
            await broadcast_status(
                project_id, AgentStepEnum.MERGE, StatusEnum.RUNNING, 98,
                "Synthesizing final Startup Blueprint and executive summary..."
            )
            
            executive_summary = (
                f"Synovia Blueprint for '{idea}': An innovative AI-native solution targeting a "
                f"{research_data.get('market_size', {}).get('tam', 'multi-billion dollar')} opportunity. "
                f"Built with {architect_data.get('frontend', {}).get('technology', 'Next.js 15')} and "
                f"{architect_data.get('backend', {}).get('technology', 'FastAPI')}, backed by a 4-week agile roadmap."
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
                "architect": architect_data,
                "roadmap": roadmap_data,
                "pitch": pitch_data
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
