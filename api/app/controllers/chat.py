from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.models.chat import Chat
from app.models.event import (
    Message,
    UserMessage,
    AssistantMessage,
    SystemMessage,
    ToolMessage,
)
from app.controllers.mixins.database_mixin import DatabaseMixin
from app.controllers.project import ProjectController
from app.http_errors import not_found
from app.schemas.chat_schemas import MessageCreate, ChatCreate, ChatRead

if TYPE_CHECKING:
    from app.models.user import ScopedActor


class ChatController(DatabaseMixin):

    def get_chat_for_actor(self, chat_id: str, actor: "ScopedActor"):
        """retrieve a chat if the actor can access it"""
        query = Chat.apply_access_predicate(select(Chat), actor, "read")
        try:
            return self.db_session.execute(query.where(Chat.uid == chat_id)).one()
        except (NoResultFound, MultipleResultsFound) as e:
            not_found(e=e)

    def create_chat_for_actor(self, chat_data: ChatCreate, actor: "ScopedActor") -> ChatRead:
        # make sure actor can access the project first
        project = ProjectController(self.db_session).read_for_actor(actor, chat_data.project_id)
        chat = Chat(
            created_by=actor.uid,
            last_updated_by=actor.uid,
            project_id=project.uid,
            **chat_data.model_dump(exclude_none=True, exclude={"project_id"})
        ).create(self.db_session)

        return ChatRead.model_validate(chat)



    def add_message(self, chat_id: str, message_data: MessageCreate) -> Message:
        message_class = {
            "user": UserMessage,
            "assistant": AssistantMessage,
            "system": SystemMessage,
            "tool": ToolMessage,
        }.get(message_data.role)

        message = message_class(
            chat_id=chat_id, **message_data.model_dump(exclude={"role"})
        )
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)
        return message
