from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.models.chat import Chat
from app.models.message import Message
from app.controllers.mixins.database_mixin import DatabaseMixin
from app.controllers.project import ProjectController
from app.http_errors import not_found
from app.schemas.chat_schemas import MessageCreate, ChatCreate, ChatRead

if TYPE_CHECKING:
    from app.models.user import ScopedActor


class ChatController(DatabaseMixin):

    def get_chat_for_actor(self, chat_id: str, actor: "ScopedActor") -> Chat:
        """retrieve a chat if the actor can access it"""
        query = Chat.apply_access_predicate(select(Chat), actor, "read")
        try:
            chat_uid = Chat.to_uid(chat_id)
            return self.db_session.execute(query.where(Chat.uid == chat_uid)).one()
        except (NoResultFound, MultipleResultsFound) as e:
            not_found(e=e)

    def create_chat_for_actor(self, chat_data: ChatCreate, actor: "ScopedActor") -> Chat:
        # make sure actor can access the project first
        project = ProjectController(self.db_session).read_for_actor(actor, chat_data.project_id)
        return Chat(
            creator_id=actor.id,
            editor_id=actor.id,
            project_id=project.id,
            **chat_data.model_dump(exclude_none=True, exclude={"project_id"})
        ).create(self.db_session)

    def update_chat_for_actor(self, chat_data: ChatCreate, actor: "ScopedActor") -> Chat:
        # make sure actor can access the project first
        chat = self.get_chat_for_actor(chat_data.id, actor)
        chat.editor_id = actor.id
        for key, value in chat_data.model_dump(exclude_none=True).items():
            setattr(chat, key, value)
        return chat.update(self.db_session)

    def add_message(self, chat_id: str, message_data: MessageCreate) -> Message:
        message = Message()
        message_class = .get(message_data.role)

        message = message_class(
            chat_id=chat_id, **message_data.model_dump(exclude={"role"})
        )
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)
        return message
