from typing import Optional, TYPE_CHECKING
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.models.project import Project
from app.controllers.mixins.collection_mixin import CollectionMixin
from app.schemas.collection_schemas import CollectionResponse, CollectionRequest
from app.schemas.user_schemas import ScopedUser
from app.schemas.project_schemas import ProjectRead
from app.http_errors import bad_request, not_found

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class ProjectController(CollectionMixin):

    def __init__(self, db_session: "Session"):
        super().__init__(db_session=db_session, ModelClass=Project)

    def list_for_actor(self, request: "CollectionRequest") -> "CollectionResponse":
        items, page_count = self.get_collection(request)
        refined_items = [ProjectRead(id=item.id, name=item.name, avatarUrl=item.avatar_url, description=item.description, organizationId=item.organization.id) for item in items]
        return CollectionResponse(items=refined_items, page=request.page, pages=page_count)

    def read_for_actor(self, actor: ScopedUser, project_id: str) -> Optional["Project"]:
        self.db_session.merge(actor.organization)
        try:
            uid = Project.id_to_uid(project_id)
        except ValueError as e:
            bad_request(e=e, message="Invalid project id")
        try:
            # TODO: use the predicate method to check if the actor has access to the project
            bound_org = actor.organization.read(self.db_session, uid=actor.organization.uid)
            self.db_session.add(bound_org)
            return bound_org.projects.filter_by(uid=uid).one()
        except (NoResultFound, MultipleResultsFound) as e:
            not_found(e=e, message="Project not found")
