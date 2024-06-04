from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends

from app.controllers.thread import ThreadController, ThreadMessageController
from app.routers.utilities import (
    list_router_for_actor_factory,
    create_router_for_actor_factory,
    read_router_for_actor_factory,
    update_router_for_actor_factory,
    delete_router_for_actor_factory,
    get_db_session,
    get_current_user,
)
from app.schemas.thread_schemas import ThreadRead, ThreadCreate, ThreadUpdate
from app.schemas.collection_schemas import CollectionResponse, CollectionRequest


if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from app.schemas.user_schemas import ScopedUser

router = APIRouter(prefix="/threads", tags=["threads"])

list_threads = list_router_for_actor_factory(ThreadController)
create_thread = create_router_for_actor_factory(ThreadController, ThreadCreate)
read_thread = read_router_for_actor_factory(ThreadController)
update_thread = update_router_for_actor_factory(ThreadController, ThreadUpdate)
delete_thread = delete_router_for_actor_factory(ThreadController)


router.get(
    "/",
    response_model=CollectionResponse,
    description="get a collection of threads scoped to the current actor",
)(list_threads)
router.post("/", response_model=ThreadRead, description="create a new thread")(
    create_thread
)
router.get(
    "/{thread_id}", response_model=ThreadRead, description="read a single thread by id"
)(read_thread)
router.post(
    "/{thread_id}",
    response_model=ThreadRead,
    description="update a single thread by id",
)(update_thread)
router.put(
    "/{thread_id}",
    response_model=ThreadRead,
    description="update a single thread by id",
)(update_thread)
router.delete(
    "/{thread_id}", response_model=None, description="delete a single thread by id"
)(delete_thread)


# get messages
@router.get(
    "/{thread_id}/messages",
    response_model=CollectionResponse,
    description="get a collection of messages in a thread",
)
def get_thread_messages(
    thread_id: str,
    perPage: int = None,
    page: int = None,
    query: str = None,
    orderBy: str = None,
    orderDir: str = None,
    db_session: "Session" = Depends(get_db_session),
    actor: "ScopedUser" = Depends(get_current_user),
):
    query_args = {}
    # drop the None values
    for key in ["perPage", "page", "orderBy", "orderDir"]:
        if locals()[key] is not None:
            query_args[key] = locals()[key]
    request = CollectionRequest(actor=actor, **query_args)
    controller = ThreadMessageController(db_session)
    return controller.list_messages_for_actor(thread_id, request)


# add message
@router.post(
    "/{thread_id}/messages/{message_id}",
    response_model=ThreadRead,
    description="add a message to a thread",
)
def add_thread_message(
    thread_id: str,
    message_id: str,
    actor: "ScopedUser" = Depends(get_current_user),
    db_session: "Session" = Depends(get_db_session),
):
    controller = ThreadMessageController(db_session)
    return controller.add_message_for_actor(thread_id, message_id, actor)


# remove message
@router.delete(
    "/{thread_id}/messages/{message_id}",
    response_model=ThreadRead,
    description="remove a message from a thread",
)
def remove_thread_message(
    thread_id: str,
    message_id: str,
    actor: "ScopedUser" = Depends(get_current_user),
    db_session: "Session" = Depends(get_db_session),
):
    controller = ThreadMessageController(db_session)
    return controller.remove_message_for_actor(thread_id, message_id, actor)
