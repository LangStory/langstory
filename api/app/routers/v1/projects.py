from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.models.project import Project
from app.schemas.project_schemas import ProjectCreate, ProjectRead

from app.routers.utilities import get_db_session, get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectRead)
def create_project(
        project_data: ProjectCreate,
        db: Session = Depends(get_db_session),
        actor: str = Depends(get_current_user),
):
    return Project(**project_data.model_dump(exclude_none=True)).create(db)


@router.get("/", response_model=List[ProjectRead])
def get_projects(db: Session = Depends(get_db_session), ):
    return Project.list(db)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(uid: UUID, db: Session = Depends(get_db_session)):
    project = Project.read(db, uid)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
