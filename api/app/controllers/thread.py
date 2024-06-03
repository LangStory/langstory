from typing import TYPE_CHECKING
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import select


from app.controllers.mixins.collection_mixin import CollectionMixin
from app.models.thread import Thread
from app.models.message import Message
from app.schemas.chat_schemas import MessageRead
from app.schemas.thread_schemas import ThreadRead, ThreadCreate, ThreadUpdate
from app.schemas.collection_schemas import CollectionResponse, CollectionRequest
from app.http_errors import not_found

from app.controllers.chat import MessageController


if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from app.schemas.user_schemas import ScopedUser


class ThreadController(CollectionMixin):

    def __init__(self, db_session: "Session"):
        super().__init__(db_session=db_session, ModelClass=Thread)

    def list_for_actor(self, request: "CollectionRequest") -> "CollectionResponse":
        items, page_count = self.get_collection(request)
        refined_items = [
            ThreadRead(
                id=item.id,
                name=item.name,
                chatId=item.chat_id,
                message_ids=[message.id for message in item.messages],
            )
            for item in items
        ]
        return CollectionResponse(
            items=refined_items, page=request.page, pages=page_count
        )

    def _get_for_actor(self, actor: "ScopedUser", thread_id: str) -> "ThreadRead":
        query = Thread.apply_access_predicate(select(Thread), actor, ["read"])
        try:
            thread_uid = Thread.to_uid(thread_id)
            return self.db_session.execute(
                query.where(Thread.uid == thread_uid)
            ).scalar_one()
        except (NoResultFound, MultipleResultsFound) as e:
            not_found(e=e)

    def read_for_actor(self, actor: "ScopedUser", thread_id: str) -> "ThreadRead":
        thread = self._get_for_actor(actor, thread_id)
        return ThreadRead(
            id=thread.id,
            name=thread.name,
            chatId=thread.chat_id,
            messageIds=[message.id for message in thread.messages],
        )

    def create_for_actor(
        self, actor: "ScopedUser", thread_data: ThreadCreate
    ) -> "ThreadRead":
        thread = Thread(
            **thread_data.model_dump(exclude_none=True, exclude=["id", "message_ids"])
        ).create(self.db_session)
        message_controller = MessageController(self.db_session)
        current_messages = []
        for message_id in thread_data.message_ids:
            message = message_controller._get_for_actor(actor, message_id)
            current_messages.append(message)
        thread.messages = current_messages
        thread = thread.update(self.db_session)
        return ThreadRead(
            id=thread.id,
            name=thread.name,
            chatId=thread.chat_id,
            messageIds=[message.id for message in thread.messages],
        )

    def update_for_actor(
        self, actor: "ScopedUser", thread_id: str, thread_data: ThreadUpdate
    ) -> "ThreadRead":
        thread = self._get_for_actor(actor, thread_id)
        for key, value in thread_data.model_dump(
            exclude_none=True, exclude=["id", "chat_id", "message_ids"]
        ).items():
            setattr(thread, key, value)
        message_controller = MessageController(self.db_session)
        current_messages = []
        for message_id in thread_data.message_ids:
            message = message_controller._get_for_actor(actor, message_id)
            current_messages.append(message)
        thread.messages = current_messages
        thread = thread.update(self.db_session)
        return ThreadRead(
            id=thread_id,
            name=thread.name,
            chatId=thread.chat_id,
            messageIds=[message.id for message in thread.messages],
        )

    def delete_for_actor(self, actor: "ScopedUser", thread_id: str) -> None:
        thread = self._get_for_actor(actor, thread_id)
        thread.deleted = True
        thread.update(self.db_session)


class ThreadMessageController(CollectionMixin):

    def __init__(self, db_session: "Session"):
        super().__init__(db_session=db_session, ModelClass=Message)

    def list_messages_for_actor(
        self, thread_id: str, request: "CollectionRequest"
    ) -> "CollectionResponse":
        select_ = select(Message).where(Message._thread_uid == Thread.to_uid(thread_id))
        items, page_count = self.get_collection(request, select_=select_)
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

    def add_message_for_actor(
        self, thread_id: str, message_id: str, actor: "ScopedUser"
    ) -> "ThreadRead":
        thread = ThreadController(self.db_session)._get_for_actor(actor, thread_id)
        message = MessageController(self.db_session)._get_for_actor(actor, message_id)
        thread.messages.append(message)
        thread.update(self.db_session)
        return ThreadRead(
            id=thread.id,
            name=thread.name,
            chatId=thread.chat_id,
            messageIds=[message.id for message in thread.messages],
        )

    def remove_message_for_actor(
        self, thread_id: str, message_id: str, actor: "ScopedUser"
    ) -> "ThreadRead":
        thread = ThreadController(self.db_session)._get_for_actor(actor, thread_id)
        for message in thread.messages:
            if message.id == message_id:
                thread.messages.remove(message)
        thread.update(self.db_session)
        return ThreadRead(
            id=thread.id,
            name=thread.name,
            chatId=thread.chat_id,
            messageIds=[message.id for message in thread.messages],
        )
