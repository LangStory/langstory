from typing import TYPE_CHECKING
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import select


from app.controllers.mixins.collection_mixin import CollectionMixin
from app.models.tool import Tool
from app.schemas.tool_schemas import ToolRead, ToolCreate, ToolUpdate
from app.schemas.collection_schemas import CollectionResponse, CollectionRequest
from app.http_errors import not_found


if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from app.schemas.user_schemas import ScopedActor


class ToolController(CollectionMixin):

    def __init__(self, db_session: "Session"):
        super().__init__(db_session=db_session, ModelClass=Tool)

    def list_for_actor(self, request: "CollectionRequest") -> "CollectionResponse":
        items, page_count = self.get_collection(request)
        refined_items = [
            ToolRead(
                id=item.id,
                name=item.name,
                description=item.description,
                projectId=item.project_id,
                jsonSchema=item.json_schema,
            )
            for item in items
        ]
        return CollectionResponse(
            items=refined_items, page=request.page, pages=page_count
        )

    def _get_for_actor(self, actor: "ScopedActor", tool_id: str) -> "ToolRead":
        query = Tool.apply_access_predicate(select(Tool), actor, ["read"])
        try:
            tool_uid = Tool.to_uid(tool_id)
            return self.db_session.execute(
                query.where(Tool.uid == tool_uid)
            ).scalar_one()
        except (NoResultFound, MultipleResultsFound) as e:
            not_found(e=e)

    def read_for_actor(self, actor: "ScopedActor", tool_id: str) -> "ToolRead":
        tool = self._get_for_actor(actor, tool_id)
        return ToolRead(
            id=tool.id,
            name=tool.name,
            projectId=tool.project_id,
            description=tool.description,
            jsonSchema=tool.json_schema,
        )

    def create_for_actor(
        self, actor: "ScopedActor", tool_data: ToolCreate
    ) -> "ToolRead":
        tool = Tool(**tool_data.model_dump(exclude_none=True)).create(self.db_session)
        self.db_session.add(tool)
        self.db_session.refresh(tool)
        return ToolRead(
            id=tool.id,
            projectId=tool.project_id,
            name=tool.name,
            description=tool.description,
            jsonSchema=tool.json_schema,
        )

    def update_for_actor(
        self, actor: "ScopedActor", tool_id: str, tool_data: ToolUpdate
    ) -> "ToolRead":
        tool = self._get_for_actor(actor, tool_id)
        for key, value in tool_data.model_dump(
            exclude_none=True, exclude=["id", "project_id"]
        ).items():
            setattr(tool, key, value)
        tool = tool.update(self.db_session)
        return ToolRead(
            id=tool_id,
            name=tool.name,
            projectId=tool.project_id,
            description=tool.description,
            jsonSchema=tool.json_schema,
        )

    def delete_for_actor(self, actor: "ScopedActor", tool_id: str) -> None:
        tool = self._get_for_actor(actor, tool_id)
        tool.deleted = True
        tool.update(self.db_session)
