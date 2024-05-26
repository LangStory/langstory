from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, TYPE_CHECKING
from uuid import UUID
from app.models.project import Project
from app.schemas.project_schemas import ProjectCreate, ProjectRead
from app.schemas.user_schemas import ScopedUser
from app.http_errors import not_found

from app.routers.utilities import get_db_session, get_current_user

if TYPE_CHECKING:
    from sqlalchemy.exc import NoInstanceFound, MultipleInstancesFound

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectRead)
def create_project(
    project_data: ProjectCreate,
    db_session: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    # since the scoped user is from the jwt and detached, we need to connect it
    db_session.merge(actor.organization)
    ## TODO: this goes in a controller since it's business logic
    return Project(
        organization_id=actor.organization.uid,
        # especially this part
        created_by=actor.uid,
        last_updated_by=actor.uid,
        **project_data.model_dump(exclude_none=True)).create(db_session)


@router.get("/", response_model=List[ProjectRead])
def get_projects(
    db_session: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    db_session.merge(actor.organization)
    return actor.organization.projects.all()


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(uid: UUID,
                actor: ScopedUser = Depends(get_current_user),
                db_session: Session = Depends(get_db_session)):
    db_session.merge(actor.organization)
    try:
        return actor.organization.projects.filter_by(uid=uid).one()
    except (NoInstanceFound, MultipleInstancesFound) as e:
        not_found(e=e, message="Project not found")