import uuid
import json
import asyncio
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response, Query, Header
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from app.database.session import get_db
from app.database.models import ProjectDB
from app.models.schemas import ProjectCreate, ProjectResponse, StatusEnum, AgentStepEnum
from app.agents.manager import manager_agent, register_sse_listener, unregister_sse_listener
from app.tools.report_generator import PDFReportGenerator
from app.core.security import extract_token_from_header, decode_access_token

logger = logging.getLogger("synovia.router.projects")
router = APIRouter(prefix="/api/projects", tags=["Projects"])

def get_current_user_id(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """Helper to extract user_id from Authorization Bearer token header."""
    token = extract_token_from_header(authorization)
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None
    return payload["sub"]

@router.post("", response_model=ProjectResponse, status_code=201)
@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    payload: ProjectCreate,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a new startup blueprint project and attaches current user_id.
    """
    user_id = get_current_user_id(authorization) or "guest"
    project_id = str(uuid.uuid4())

    new_project = ProjectDB(
        id=project_id,
        user_id=user_id,
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
    limit: int = Query(200, ge=1, le=1000, description="Max history items to return."),
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves project history strictly isolated for the logged-in user.
    One user cannot view data belonging to another user.
    """
    user_id = get_current_user_id(authorization)

    # Filter strictly by user_id if logged in, or guest/unassigned if guest
    if user_id:
        stmt = select(ProjectDB).where(ProjectDB.user_id == user_id).order_by(ProjectDB.created_at.desc()).limit(limit)
    else:
        stmt = select(ProjectDB).where((ProjectDB.user_id == "guest") | (ProjectDB.user_id == None)).order_by(ProjectDB.created_at.desc()).limit(limit)

    result = await db.execute(stmt)
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
async def get_project(
    project_id: str, 
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Fetches project blueprint details after validating user ownership.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    user_id = get_current_user_id(authorization)
    # Enforce isolation: if project is owned by a specific user, verify user matches
    if project.user_id and project.user_id != "guest":
        if not user_id or user_id != project.user_id:
            raise HTTPException(status_code=403, detail="Access denied: You do not have permission to view this project.")

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
async def clear_all_projects(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Deletes all projects belonging to the current user.
    """
    user_id = get_current_user_id(authorization) or "guest"
    await db.execute(delete(ProjectDB).where(ProjectDB.user_id == user_id))
    await db.commit()
    return Response(status_code=204)

@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str, 
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Deletes a specific project after verifying user ownership.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    user_id = get_current_user_id(authorization)
    if project.user_id and project.user_id != "guest":
        if not user_id or user_id != project.user_id:
            raise HTTPException(status_code=403, detail="Access denied: You do not have permission to delete this project.")

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

@router.get("/{project_id}/ppt")
async def download_project_ppt(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Generates and returns a 16:9 Widescreen PowerPoint (.pptx) Pitch Deck.
    """
    from app.tools.ppt_generator import ppt_report_generator
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    project = result.scalars().first()
    if not project or not project.blueprint_json:
        raise HTTPException(status_code=404, detail="Project blueprint not ready or not found")

    ppt_bytes = ppt_report_generator.create_deck(project.blueprint_json)

    filename = f"Synovia_Pitch_Deck_{project.idea[:15].replace(' ', '_')}.pptx"
    return Response(
        content=ppt_bytes,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
