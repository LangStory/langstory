from typing import TYPE_CHECKING, List, Union, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.controllers.mixins.database_mixin import DatabaseMixin
from app.controllers.mixins.collection_mixin import CollectionMixin
from app.controllers.project import ProjectController
from app.http_errors import not_found
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.chat_schemas import (
    MessageCreate,
    ChatCreate,
    ChatRead,
    ToolCallCreate,
    MessageRead,
    MessageUpdate
)
from app.schemas.collection_schemas import CollectionResponse, CollectionRequest

if TYPE_CHECKING:
    from app.schemas.user_schemas import ScopedUser
    from app.models.tool_call import ToolCall
    from sqlalchemy.orm import Session


class ChatController(CollectionMixin, DatabaseMixin):

    def __init__(self, db_session: "Session"):
        super().__init__(db_session=db_session, ModelClass=Chat)

    def list_for_actor(self, request: "CollectionRequest") -> "CollectionResponse":
        items, page_count = self.get_collection(request)
        refined_items = [
            ChatRead(
                id=item.id,
                name=item.name,
                project_id=item.project_id,
            )
            for item in items
        ]
        return CollectionResponse(
            items=refined_items, page=request.page, pages=page_count
        )

    def get_chat_for_actor(self, chat_id: str, actor: "ScopedUser") -> Chat:
        """retrieve a chat if the actor can access it"""
        query = Chat.apply_access_predicate(select(Chat), actor, ["read"])
        try:
            chat_uid = Chat.to_uid(chat_id)
            return self.db_session.execute(
                query.where(Chat.uid == chat_uid)
            ).scalar_one()
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
        chat = self.get_chat_for_actor(chat_id, actor)

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

        for tool_call in message_data.tool_calls_requested or []:
            tool_call = self._to_tool_call(tool_call, message.id)
        self.db_session.add(message)
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


class MessageController(CollectionMixin):

    def __init__(self, db_session: "Session"):
        super().__init__(db_session=db_session, ModelClass=Message)


    def get_message_for_actor(self, message_id: str, actor: "ScopedUser") -> Message:
        """retrieve a message if the actor can access it"""
        query = Message.apply_access_predicate(select(Message), actor, ["read"])
        try:
            message_uid = Message.to_uid(message_id)
            return self.db_session.execute(
                query.where(Message.uid == message_uid)
            ).scalar_one()
        except (NoResultFound, MultipleResultsFound) as e:
            not_found(e=e)

    def list_chat_messages_for_actor(
        self, chat_id: str, request: "CollectionRequest"
    ) -> CollectionResponse:
        chat = ChatController(self.db_session).get_chat_for_actor(
            chat_id, request.actor
        )
        items, page_count = self.get_collection(request, select_=chat.messages)
        refined_items = [
            MessageRead(
                id=item.id,
                type=item.type,
                timestamp=item.timestamp,
                content=item.content,
                chat_id=item.chat_id,
            )
            for item in items
        ]
        return CollectionResponse(
            items=refined_items, page=request.page, pages=page_count
        )

    def update_message_for_actor(self, message_data: MessageUpdate, actor: "ScopedUser") -> Message:
        # make sure actor can access the project first
        chat_controller = ChatController(self.db_session)

        chat = chat_controller.get_chat_for_actor(message_data.chat_id, actor)
        chat.editor_id = actor.id
        message = self.get_message_for_actor(message_data.id, actor)
        message.editor_id = actor.id
        for key, value in message_data.model_dump(exclude_none=True, exclude=["id","chat_id"]).items():
            setattr(message, key, value)
        self.db_session.add(chat)
        self.db_session.add(message)
        _ = chat.update(self.db_session)
        return message.update(self.db_session)
