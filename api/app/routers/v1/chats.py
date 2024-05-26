from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.chat import ChatController
from app.models.chat import Chat
from app.routers.utilities import get_db_session
from app.schemas.chat_schemas import ChatCreate, ChatRead, MessageCreate, MessageRead

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatRead)
def create_chat(chat_data: ChatCreate, db: Session = Depends(get_db_session)):
    return Chat(**chat_data.model_dump(exclude_none=True)).create(db)


@router.post("/{chat_id}/messages", response_model=MessageRead)
def add_message(
    chat_id: UUID, message_data: MessageCreate, db: Session = Depends(get_db_session)
):
    controller = ChatController(db)
    message = controller.add_message(chat_id, message_data)
    return message


@router.get("/{chat_id}/messages", response_model=List[MessageRead])
def get_messages(chat_id: UUID, db: Session = Depends(get_db_session)):
    chat = Chat.read(db, uid=chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not chat.messages:
        raise HTTPException(status_code=404, detail="No messages available for chat")
    return chat
