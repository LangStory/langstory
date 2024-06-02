from typing import TYPE_CHECKING, Union, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.controllers.mixins.database_mixin import DatabaseMixin
from app.controllers.project import ProjectController
from app.http_errors import not_found
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.chat_schemas import MessageCreate, ChatCreate, ToolCallCreate

if TYPE_CHECKING:
    from app.schemas.user_schemas import ScopedUser
    from app.models.tool_call import ToolCall


class ChatController(DatabaseMixin):

    def get_chat_for_actor(self, chat_id: str, actor: "ScopedUser") -> Chat:
        """retrieve a chat if the actor can access it"""
        query = Chat.apply_access_predicate(select(Chat), actor, ["read"])
        try:
            chat_uid = Chat.to_uid(chat_id)
            return self.db_session.execute(query.where(Chat.uid == chat_uid)).one()
        except (NoResultFound, MultipleResultsFound) as e:
            not_found(e=e)

    def create_chat_for_actor(self, chat_data: ChatCreate, actor: "ScopedUser") -> Chat:
        # make sure actor can access the project first
        project = ProjectController(self.db_session).read_for_actor(
            actor, chat_data.project_id
        )
        return Chat(
            creator_id=actor.id,
            editor_id=actor.id,
            project_id=project.id,
            **chat_data.model_dump(exclude_none=True, exclude={"project_id"})
        ).create(self.db_session)

    def update_chat_for_actor(self, chat_data: ChatCreate, actor: "ScopedUser") -> Chat:
        # make sure actor can access the project first
        chat = self.get_chat_for_actor(chat_data.id, actor)
        chat.editor_id = actor.id
        for key, value in chat_data.model_dump(exclude_none=True).items():
            setattr(chat, key, value)
        return chat.update(self.db_session)

    def add_message(
            self, chat_id: str, message_data: MessageCreate, actor: "ScopedUser"
    ) -> Message:
        chat = self.get_chat_for_actor(chat_id)

        if message_data.type == "tool_message":
            message_data.tool_call_response = self._to_tool_call(
                message_data.tool_call_response
            )

        message = Message(
            chat_id=chat.id,
            creator_id=actor.id,
            editor_id=actor.id,
            **message_data.model_dump(
                exclude={"tool_calls_requested"}, exclude_none=True
            )
        ).create(self.db_session)

        if tool_call in message_data.tool_calls_requested:
            tool_call = self._to_tool_call(tool_call, message.id)
        self.db_session.refresh(message)
        return message

    def _to_tool_call(
            self,
            tool_call: Union[ToolCallCreate, str],
            assistant_message_id: Optional[str] = None,
    ) -> "ToolCall":
        """a flexible input that takes either a definition or an existing uuid and returns the ToolCall object
        Args:
            tool_call (Union[ToolCallCreate, str]): the tool call to convert
            assistant_message_id (Optional[str], optional): the assistant message id to associate with the tool call, for creating new.
        """
        try:
            uid = ToolCall.to_uid(tool_call)
            query = ToolCall.apply_access_predicate(
                select(ToolCall).where(ToolCall.uid == uid), self.actor, "read"
            )
            return self.db_session.execute(query).one()
        except (ValueError, AttributeError):
            # not an id, so it must be a definition
            return ToolCall(**tool_call.model_dump(exclude_none=True)).create(
                self.db_session
            )
