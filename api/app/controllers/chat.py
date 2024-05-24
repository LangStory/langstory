from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.models.event import Message, UserMessage, AssistantMessage, SystemMessage, ToolMessage
from app.schemas.chat_schemas import ChatCreate, MessageCreate, MessageRead

class ChatController:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_chat(self, chat_data: ChatCreate) -> Chat:
        chat = Chat(**chat_data.dict())
        self.db_session.add(chat)
        self.db_session.commit()
        self.db_session.refresh(chat)
        return chat

    def add_message(self, chat_id: UUID, message_data: MessageCreate) -> Message:
        message_class = {
            "user": UserMessage,
            "assistant": AssistantMessage,
            "system": SystemMessage,
            "tool": ToolMessage,
        }.get(message_data.role)

        message = message_class(chat_id=chat_id, **message_data.dict(exclude={"role"}))
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)
        return message

    def get_messages(self, chat_id: UUID) -> List[MessageRead]:
        messages = self.db_session.query(Message).filter(Message.chat_id == chat_id).all()
        return [MessageRead.from_orm(msg) for msg in messages]
