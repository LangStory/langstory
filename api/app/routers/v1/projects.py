from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.controllers.project import ProjectController
from app.schemas.project_schemas import ProjectCreate, ProjectRead

from app.routers.utilities import get_db_session

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectRead)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db_session)):
    controller = ProjectController(db)
    project = controller.create_project(project_data)
    return project


@router.get("/", response_model=List[ProjectRead])
def get_projects(db: Session = Depends(get_db_session)):
    controller = ProjectController(db)
    projects = controller.get_projects()
    return projects


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: UUID, db: Session = Depends(get_db_session)):
    controller = ProjectController(db)
    project = controller.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
