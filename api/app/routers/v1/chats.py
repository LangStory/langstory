from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.chat import ChatController
from app.routers.utilities import get_db_session
from app.schemas.chat_schemas import ChatCreate, ChatRead, MessageCreate, MessageRead

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatRead)
def create_chat(chat_data: ChatCreate, db: Session = Depends(get_db_session)):
    controller = ChatController(db)
    chat = controller.create_chat(chat_data)
    return chat


@router.post("/{chat_id}/messages", response_model=MessageRead)
def add_message(chat_id: UUID, message_data: MessageCreate, db: Session = Depends(get_db_session)):
    controller = ChatController(db)
    message = controller.add_message(chat_id, message_data)
    return message


@router.get("/{chat_id}/messages", response_model=List[MessageRead])
def get_messages(chat_id: UUID, db: Session = Depends(get_db_session)):
    controller = ChatController(db)
    messages = controller.get_messages(chat_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Chat not found or no messages available")
    return messages
