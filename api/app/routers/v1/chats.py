from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.chat import ChatController, MessageController
from app.models.chat import Chat
from app.routers.utilities import get_db_session, get_current_user
from app.schemas.chat_schemas import (
    ChatCreate,
    ChatRead,
    MessageCreate,
    MessageRead,
    MessageUpdate,
)
from app.schemas.user_schemas import ScopedUser
from app.schemas.collection_schemas import CollectionResponse, CollectionRequest

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("/", response_model=CollectionResponse)
def list_chats(
    perPage: int = None,
    page: int = None,
    query: str = None,
    orderBy: str = None,
    orderDir: str = None,
    db_session: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    query_args = {}
    # drop the None values
    for key in ["perPage", "page", "orderBy", "orderDir"]:
        if locals()[key] is not None:
            query_args[key] = locals()[key]
    request = CollectionRequest(actor=actor, **query_args)
    controller = ChatController(db_session)
    return controller.list_for_actor(request)


@router.get("/{chat_id}", response_model=ChatRead)
def get_chat(
    chat_id: str,
    db: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    controller = ChatController(db)
    chat = controller.get_chat_for_actor(chat_id, actor)
    return chat


@router.post("/")
def create_chat(
    chat_data: ChatCreate,
    db_session: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    controller = ChatController(db_session)
    chat = controller.create_chat_for_actor(chat_data, actor)
    return ChatRead(
        id=chat.id,
        name=chat.name,
        description=chat.description,
        project_id=chat_data.project_id,  # need to do this explicitly because it is a prop
    )


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
def delete_chat(
    chat_id: str,
    db: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
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


@router.get("/{chat_id}/messages", response_model=CollectionResponse)
def list_messages(
    chat_id: str,
    perPage: int = None,
    page: int = None,
    query: str = None,
    orderBy: str = None,
    orderDir: str = None,
    db_session: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    query_args = {}
    # drop the None values
    for key in ["perPage", "page", "orderBy", "orderDir"]:
        if locals()[key] is not None:
            query_args[key] = locals()[key]
    request = CollectionRequest(actor=actor, **query_args)
    controller = MessageController(db_session)
    return controller.list_chat_messages_for_actor(chat_id, request)


@router.put("/{chat_id}/messages/{message_id}", response_model=MessageRead)
@router.patch("/{chat_id}/messages/{message_id}", response_model=MessageRead)
def update_message(
    chat_id: str,
    message_id: str,
    message_data: MessageUpdate,
    db: Session = Depends(get_db_session),
    actor: ScopedUser = Depends(get_current_user),
):
    message_data.id = message_id
    message_data.chat_id = chat_id
    controller = MessageController(db)
    message = controller.update_message_for_actor(message_data, actor)
    extra = {}
    match message.type:
        case "user_message":
            extra["persona"] = message.persona
        case "assistant_message":
            extra["tool_calls_requested"] = message.tool_calls_requested
        case "tool_message":
            extra["tool_call_response"] = message.tool_call_response
        case _:
            pass
    return MessageRead(
        id=message.id,
        name=message.name,
        chat_id=chat_id,
        type=message.type,
        timestamp=message.timestamp,
        content=message.content,
        **extra,
    )
