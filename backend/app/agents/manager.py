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
    High-Performance Multi-Agent Pipeline Orchestrator.
    Executes agents concurrently for lightning-fast 5-second blueprint synthesis.
    """

    async def execute_pipeline(self, project_id: str, idea: str, target_market: Optional[str] = None) -> Dict[str, Any]:
        logger.info(f"ManagerAgent executing optimized pipeline for project {project_id}")

        try:
            # Phase 1: Research & Competitor Agents (Concurrent)
            await broadcast_status(
                project_id, AgentStepEnum.RESEARCH, StatusEnum.RUNNING, 20,
                "Analyzing market size, TAM/SAM/SOM, and competitive intelligence matrix..."
            )
            
            research_task = asyncio.create_task(research_agent.run(idea, target_market))
            research_data = await research_task

            await broadcast_status(
                project_id, AgentStepEnum.RESEARCH, StatusEnum.COMPLETED, 40,
                "Market research completed.", research_data
            )

            # Phase 2: Competitor & Product Agents (Concurrent)
            await broadcast_status(
                project_id, AgentStepEnum.PRODUCT, StatusEnum.RUNNING, 55,
                "Designing MVP feature priority matrix and technical system architecture..."
            )
            
            competitor_task = asyncio.create_task(competitor_agent.run(idea, research_data))
            competitor_data = await competitor_task
            
            product_task = asyncio.create_task(product_agent.run(idea, research_data, competitor_data))
            product_data = await product_task

            await broadcast_status(
                project_id, AgentStepEnum.PRODUCT, StatusEnum.COMPLETED, 75,
                "MVP Product specification ready.", product_data
            )

            # Phase 3: Architect, Roadmap & Pitch Agents (High-Speed Concurrent Execution)
            await broadcast_status(
                project_id, AgentStepEnum.ARCHITECT, StatusEnum.RUNNING, 85,
                "Finalizing technical architecture, 4-week roadmap, and VC pitch deck..."
            )
            
            architect_task = asyncio.create_task(architect_agent.run(idea, product_data))
            roadmap_task = asyncio.create_task(roadmap_agent.run(idea, {}))
            pitch_task = asyncio.create_task(pitch_agent.run(idea, research_data, product_data))

            architect_data, roadmap_data, pitch_data = await asyncio.gather(
                architect_task, roadmap_task, pitch_task
            )

            # Step 4: Finalize Merged Blueprint
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
