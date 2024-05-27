from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.project import Project
from app.controllers.project import ProjectController

from app.schemas.project_schemas import ProjectCreate, ProjectRead
from app.schemas.user_schemas import ScopedUser
from app.schemas.collection_schemas import CollectionResponse, CollectionRequest

from app.routers.utilities import get_db_session, get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/")
def create_project(
    project_data: ProjectCreate,
    db_session: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
)-> ProjectRead:
    # since the scoped user is from the jwt and detached, we need to connect it
    db_session.merge(actor.organization)
    ## TODO: this goes in a controller since it's business logic
    project =  Project(
        organization_id=actor.organization.uid,
        # especially this part
        created_by=actor.uid,
        last_updated_by=actor.uid,
        **project_data.model_dump(exclude_none=True)
    ).create(db_session)
    db_session.add(project)
    db_session.refresh(project)
    return ProjectRead(id=project.id, name=project.name, avatarUrl=project.avatar_url, description=project.description, organizationId=project.organization.id)

@router.get("/", response_model=CollectionResponse)
def list_projects(
    perPage: int = None,
    page: int = None,
    query: str = None,
    orderBy: str = None,
    orderDir: str = None,
    db_session: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    query_args = {}
    # drop the None values
    for key in ["perPage", "page", "orderBy", "orderDir"]:
        if locals()[key] is not None:
            query_args[key] = locals()[key]
    request = CollectionRequest(actor=actor, **query_args)
    controller = ProjectController(db_session)
    return controller.list_for_actor(request)


@router.get("/{project_id}", response_model=ProjectRead)
def read_project(
    project_id: str,
    actor: ScopedUser = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
):

    controller = ProjectController(db_session)
    return controller.read_for_actor(actor, project_id)
