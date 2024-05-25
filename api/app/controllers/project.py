from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project_schemas import ProjectCreate, ProjectRead


class ProjectController:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_project(self, project_data: ProjectCreate) -> Project:
        project = Project(**project_data.dict())
        self.db_session.add(project)
        self.db_session.commit()
        self.db_session.refresh(project)
        return project

    def get_projects(self) -> List[ProjectRead]:
        projects = self.db_session.query(Project).all()
        return [ProjectRead.from_orm(proj) for proj in projects]

    def get_project(self, project_id: UUID) -> ProjectRead:
        project = self.db_session.query(Project).filter(Project.uid == project_id).first()
        if project:
            return ProjectRead.from_orm(project)
        return None
