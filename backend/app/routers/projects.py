import uuid
import json
import asyncio
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.session import get_db
from app.database.models import ProjectDB
from app.models.schemas import ProjectCreate, ProjectResponse, StatusEnum, AgentStepEnum
from app.agents.manager import manager_agent, register_sse_listener, unregister_sse_listener
from app.tools.report_generator import PDFReportGenerator

logger = logging.getLogger("synovia.router.projects")
router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.post("", response_model=ProjectResponse, status_code=201)
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
async def list_projects(db: AsyncSession = Depends(get_db)):
    """
    Retrieves all past generated startup projects.
    """
    result = await db.execute(select(ProjectDB).order_by(ProjectDB.created_at.desc()))
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

@router.get("/{project_id}/stream")
async def stream_project_execution(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Server-Sent Events (SSE) endpoint providing real-time multi-agent execution updates.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    async def event_generator():
        queue = asyncio.Queue()
        register_sse_listener(project_id, queue)
        
        try:
            # Yield historical logs first for reconnection resilience
            if project.step_logs_json:
                for log in project.step_logs_json:
                    yield f"data: {json.dumps(log)}\n\n"
            
            # If already completed or failed, close stream
            if project.status in [StatusEnum.COMPLETED.value, StatusEnum.FAILED.value]:
                return

            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
                if data.get("step") == AgentStepEnum.COMPLETED.value or data.get("status") == StatusEnum.FAILED.value:
                    break
        finally:
            unregister_sse_listener(project_id, queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/{project_id}/pdf")
async def download_project_pdf(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Generates and downloads investor-ready PDF startup blueprint.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    project = result.scalars().first()
    if not project or not project.blueprint_json:
        raise HTTPException(status_code=404, detail="Project blueprint not ready or not found")

    pdf_bytes = PDFReportGenerator.generate_startup_blueprint_pdf(project.blueprint_json)
    filename = f"synovia-blueprint-{project_id[:8]}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
