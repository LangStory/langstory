from typing import Optional, TYPE_CHECKING
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.models.project import Project
from app.controllers.mixins.collection_mixin import CollectionMixin
from app.schemas.collection_schemas import CollectionResponse, CollectionRequest
from app.schemas.user_schemas import ScopedUser
from app.http_errors import bad_request, not_found

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class ProjectController(CollectionMixin):

    def __init__(self, db_session: "Session"):
        self.super().__init__(db_session=db_session, model=Project)

    def list_for_actor(self, request: "CollectionRequest") -> "CollectionResponse":
        return self.get_collection(request)

    def read_for_actor(self, actor:ScopedUser, project_id: str) -> Optional["Project"]:
        self.db_session.merge(actor.organization)
        try:
            uid = Project.id_to_uid(project_id)
        except ValueError as e:
            bad_request(e=e, message="Invalid project id")
        try:
            # TODO: use the predicate method to check if the actor has access to the project
            return actor.organization.projects.filter_by(uid=uid).one()
        except (NoResultFound, MultipleResultsFound) as e:
            not_found(e=e, message="Project not found")