from typing import Optional, TYPE_CHECKING
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import select

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
        refined_items = [
            ProjectRead(
                id=item.id,
                name=item.name,
                avatarUrl=item.avatar_url,
                description=item.description,
                organizationId=item.organization.id,
            )
            for item in items
        ]
        return CollectionResponse(
            items=refined_items, page=request.page, pages=page_count
        )

    def read_for_actor(self, actor: ScopedUser, project_id: str) -> Optional["Project"]:
        self.db_session.merge(actor.organization)
        try:
            project_uid = Project.to_uid(project_id)
            query = Project.apply_access_predicate(select(Project), actor, ["read"])
            project = self.db_session.execute(
                query.where(Project.uid == project_uid)
            ).scalar_one()
        except (NoResultFound, MultipleResultsFound) as e:
            not_found(e=e)
        try:
            message = (
                "Project is not in the organization the actor is currently bound to"
            )
            assert project.organization_id == actor.organization.id, message
            return project
        except AssertionError as e:
            bad_request(e=e, message=message)
