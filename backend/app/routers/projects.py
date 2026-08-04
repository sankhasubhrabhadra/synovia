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
from app.tools.ppt_generator import PPTReportGenerator

logger = logging.getLogger("synovia.router.projects")
router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("", response_model=ProjectResponse, status_code=201)
@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    payload: ProjectCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a new startup blueprint project.
    """
    project_id = str(uuid.uuid4())

    new_project = ProjectDB(
        id=project_id,
        user_id="guest",
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
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves project history.
    """
    stmt = select(ProjectDB).order_by(ProjectDB.created_at.desc()).limit(limit)
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
    db: AsyncSession = Depends(get_db)
):
    """
    Fetches project blueprint details.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    proj = result.scalar_one_or_none()
    
    if not proj:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found.")
        
    return ProjectResponse(
        id=proj.id,
        idea=proj.idea,
        status=StatusEnum(proj.status),
        current_step=AgentStepEnum(proj.current_step),
        created_at=proj.created_at.isoformat(),
        updated_at=proj.updated_at.isoformat(),
        blueprint=proj.blueprint_json
    )

@router.get("/{project_id}/stream")
async def stream_project_execution(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Server-Sent Events (SSE) streaming endpoint for live execution status updates.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    proj = result.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")

    async def event_generator():
        q: asyncio.Queue = asyncio.Queue()
        await register_sse_listener(project_id, q)
        
        initial_data = {
            "project_id": proj.id,
            "status": proj.status,
            "current_step": proj.current_step,
            "progress_percentage": proj.progress_percentage,
            "logs": proj.step_logs_json or [],
            "blueprint": proj.blueprint_json
        }
        yield f"data: {json.dumps(initial_data)}\n\n"
        
        try:
            while True:
                data = await q.get()
                yield f"data: {json.dumps(data)}\n\n"
                if data.get("status") in ["completed", "failed"]:
                    break
        except asyncio.CancelledError:
            pass
        finally:
            await unregister_sse_listener(project_id, q)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.delete("/{project_id}", status_code=204)
async def delete_single_project(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Deletes a single project blueprint from history.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    proj = result.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    await db.delete(proj)
    await db.commit()
    return Response(status_code=204)

@router.delete("", status_code=204)
@router.delete("/", status_code=204)
async def clear_all_projects(db: AsyncSession = Depends(get_db)):
    """
    Deletes all projects from history.
    """
    await db.execute(delete(ProjectDB))
    await db.commit()
    return Response(status_code=204)

@router.get("/{project_id}/pdf")
async def download_pdf_report(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Generates and downloads a formal 7-page PDF report.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    proj = result.scalar_one_or_none()
    
    if not proj or not proj.blueprint_json:
        raise HTTPException(status_code=400, detail="Blueprint data is missing or incomplete for PDF generation.")
        
    blueprint = proj.blueprint_json
    if isinstance(blueprint, dict) and "idea" not in blueprint:
        blueprint["idea"] = proj.idea
        
    pdf_bytes = PDFReportGenerator.generate_blueprint_pdf(blueprint)
    filename = f"Synovia_Blueprint_{proj.idea[:15].replace(' ', '_')}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/{project_id}/ppt")
async def download_ppt_deck(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Generates and downloads a 16:9 executive PowerPoint (.pptx) pitch deck.
    """
    result = await db.execute(select(ProjectDB).where(ProjectDB.id == project_id))
    proj = result.scalar_one_or_none()
    
    if not proj or not proj.blueprint_json:
        raise HTTPException(status_code=400, detail="Blueprint data is missing or incomplete for PPT generation.")
        
    generator = PPTReportGenerator()
    blueprint = proj.blueprint_json
    if isinstance(blueprint, dict) and "idea" not in blueprint:
        blueprint["idea"] = proj.idea
        
    ppt_bytes = generator.create_deck(blueprint)
    filename = f"Synovia_Pitch_Deck_{proj.idea[:15].replace(' ', '_')}.pptx"
    
    return Response(
        content=ppt_bytes,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
