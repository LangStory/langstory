from uuid import UUID

from sqlalchemy.orm import Session

from app.models.event import (
    Message,
    UserMessage,
    AssistantMessage,
    SystemMessage,
    ToolMessage,
)
from app.schemas.chat_schemas import MessageCreate


class ChatController:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_message(self, chat_id: UUID, message_data: MessageCreate) -> Message:
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
