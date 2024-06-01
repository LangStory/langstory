from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.chat import ChatController
from app.models.chat import Chat
from app.routers.utilities import get_db_session, get_current_user
from app.schemas.chat_schemas import ChatCreate, ChatRead, MessageCreate, MessageRead
from app.schemas.user_schemas import ScopedUser

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("/{chat_id}", response_model=ChatRead)
def get_chat(
    chat_id: str,
    db: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    controller = ChatController(db)
    chat = controller.get_chat_for_actor(chat_id, actor)
    return chat

@router.post("/", response_model=ChatRead)
def create_chat(
    chat_data: ChatCreate,
    db_session: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    controller = ChatController(db_session)
    return controller.create_chat_for_actor(chat_data, actor)

@router.put("/{chat_id}", response_model=ChatRead)
@router.patch("/{chat_id}", response_model=ChatRead)
def update_chat(
    chat_id: str,
    chat_data: ChatCreate,
    db: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    controller = ChatController(db)
    return controller.update_chat_for_actor(chat_id, chat_data, actor)

@router.delete("/{chat_id}")
def delete_chat(chat_id: str,
                db: Session = Depends(get_db_session),
                actor: ScopedUser = Depends(get_current_user)):
    controller = ChatController(db)
    chat = controller.get_chat_for_actor(chat_id, actor)
    chat.deleted = True
    chat.update(db)
    return {"message": "Chat deleted successfully"}

@router.post("/{chat_id}/messages", response_model=MessageRead)
def add_message(
    chat_id: str,
    message_data: MessageCreate,
    db: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    controller = ChatController(db)
    return controller.add_message(chat_id, message_data, actor)


@router.get("/{chat_id}/messages", response_model=List[MessageRead])
def get_messages(chat_id: str, db: Session = Depends(get_db_session)):
    chat = Chat.read(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not chat.messages:
        raise HTTPException(status_code=404, detail="No messages available for chat")
    return chat

