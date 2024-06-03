from typing import TYPE_CHECKING


from app.controllers.mixins.collection_mixin import CollectionMixin
from app.models.tool import Tool
from app.schemas.tool_schemas import ToolRead
from app.schemas.collection_schemas import CollectionResponse, CollectionRequest

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

class ToolController(CollectionMixin):

    def __init__(self, db_session: "Session"):
        super().__init__(db_session=db_session, ModelClass=Tool)

    def list_for_actor(self, request: "CollectionRequest") -> "CollectionResponse":
        items, page_count = self.get_collection(request)
        refined_items = [
            ToolRead(
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
