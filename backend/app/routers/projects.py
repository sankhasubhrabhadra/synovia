import uuid
import json
import asyncio
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from app.database.session import get_db
from app.database.models import ProjectDB
from app.models.schemas import ProjectCreate, ProjectResponse, StatusEnum, AgentStepEnum
from app.agents.manager import manager_agent, register_sse_listener, unregister_sse_listener
from app.tools.report_generator import PDFReportGenerator

logger = logging.getLogger("synovia.router.projects")
router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.post("", response_model=ProjectResponse, status_code=201)
@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    payload: ProjectCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a new startup blueprint project and launches the multi-agent pipeline asynchronously.
    """
    project_id = str(uuid.uuid4())
    new_project = ProjectDB(
        id=project_id,
        idea=payload.idea.strip(),
        status=StatusEnum.RUNNING.value,
        current_step=AgentStepEnum.MANAGER.value,
        progress_percentage=5,
        step_logs_json=[]
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    # Launch autonomous agent pipeline in background
    background_tasks.add_task(
        manager_agent.execute_pipeline,
        project_id=project_id,
        idea=payload.idea.strip(),
        target_market=payload.target_market
    )

    return ProjectResponse(
        id=new_project.id,
        idea=new_project.idea,
        status=StatusEnum(new_project.status),
        current_step=AgentStepEnum(new_project.current_step),
        created_at=new_project.created_at.isoformat(),
        updated_at=new_project.updated_at.isoformat(),
        blueprint=new_project.blueprint_json
    )

@router.get("", response_model=List[ProjectResponse])
@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    limit: int = Query(200, ge=1, le=1000, description="Max history items to return (supports 100+ work history)."),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves history of generated startup projects (supports 100+ projects).
    """
    result = await db.execute(
        select(ProjectDB)
        .order_by(ProjectDB.created_at.desc())
        .limit(limit)
    )
    projects = result.scalars().all()
    
    return [
        ProjectResponse(
            id=p.id,
            idea=p.idea,
            status=StatusEnum(p.status),
            current_step=AgentStepEnum(p.current_step),
            created_at=p.created_at.isoformat(),
            updated_at=p.updated_at.isoformat(),
            blueprint=p.blueprint_json
        )
        for p in projects
    ]

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Fetches details and generated blueprint for a specific project.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectResponse(
        id=project.id,
        idea=project.idea,
        status=StatusEnum(project.status),
        current_step=AgentStepEnum(project.current_step),
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
        blueprint=project.blueprint_json
    )

@router.delete("", status_code=204)
@router.delete("/", status_code=204)
async def clear_all_projects(db: AsyncSession = Depends(get_db)):
    """
    Deletes all projects from history database.
    """
    await db.execute(delete(ProjectDB))
    await db.commit()
    return Response(status_code=204)

@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Deletes a specific project from database history.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await db.delete(project)
    await db.commit()
    return Response(status_code=204)

@router.get("/{project_id}/stream")
async def stream_project_events(project_id: str):
    """
    Server-Sent Events (SSE) streaming endpoint for live agent execution progress.
    """
    async def event_generator():
        queue = asyncio.Queue()
        register_sse_listener(project_id, queue)
        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
                if data.get("step") == AgentStepEnum.COMPLETED.value or data.get("status") == StatusEnum.FAILED.value:
                    break
        except asyncio.CancelledError:
            pass
        finally:
            unregister_sse_listener(project_id, queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/{project_id}/pdf")
async def download_project_pdf(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Generates and returns an executive PDF report for the project blueprint.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    project = result.scalars().first()
    if not project or not project.blueprint_json:
        raise HTTPException(status_code=404, detail="Project blueprint not ready or not found")

    generator = PDFReportGenerator()
    pdf_bytes = generator.generate_blueprint_pdf(project.blueprint_json)

    filename = f"Synovia_Blueprint_{project.idea[:15].replace(' ', '_')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
