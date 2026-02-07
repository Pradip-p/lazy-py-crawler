from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.database import get_session, User, Project
from app.auth import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    data_type: str = "Generic"
    output_format: str = "CSV"
    project_type: str = "One-time"
    urls: str


class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    data_type: str
    output_format: str
    project_type: str
    urls: str
    status: str
    created_at: datetime
    mongo_collection: Optional[str] = None


@router.post("", response_model=ProjectRead)
async def create_project(
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Create a new scraping project"""
    # Create the project record in Postgres
    db_project = Project(
        user_id=current_user.id,
        name=project_in.name,
        description=project_in.description,
        data_type=project_in.data_type,
        output_format=project_in.output_format,
        project_type=project_in.project_type,
        urls=project_in.urls,
        status="Pending",
        mongo_collection=f"project_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
    )

    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)

    return db_project


@router.get("", response_model=List[ProjectRead])
async def list_projects(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """List all projects for the current user (or all projects if superuser)"""
    if current_user.is_superuser:
        statement = select(Project).order_by(Project.created_at.desc())
    else:
        statement = (
            select(Project)
            .where(Project.user_id == current_user.id)
            .order_by(Project.created_at.desc())
        )

    results = await session.exec(statement)
    projects = results.all()
    return projects


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get project details and status"""
    statement = select(Project).where(Project.id == project_id)
    result = await session.exec(statement)
    project = result.first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check orientation: owner or superuser
    if not current_user.is_superuser and project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Delete a project"""
    statement = select(Project).where(Project.id == project_id)
    result = await session.exec(statement)
    project = result.first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check orientation: owner or superuser
    if not current_user.is_superuser and project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await session.delete(project)
    await session.commit()

    return {"message": "Project deleted successfully"}
