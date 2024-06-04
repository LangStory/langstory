from fastapi import APIRouter

from app.controllers.tool import ToolController
from app.routers.utilities import (
    list_router_for_actor_factory,
    create_router_for_actor_factory,
    read_router_for_actor_factory,
    update_router_for_actor_factory,
    delete_router_for_actor_factory,
)
from app.schemas.tool_schemas import ToolRead, ToolCreate, ToolUpdate
from app.schemas.collection_schemas import CollectionResponse

router = APIRouter(prefix="/tools", tags=["tools"])

list_tools = list_router_for_actor_factory(ToolController)
create_tool = create_router_for_actor_factory(ToolController, ToolCreate)
read_tool = read_router_for_actor_factory(ToolController)
update_tool = update_router_for_actor_factory(ToolController, ToolUpdate)
delete_tool = delete_router_for_actor_factory(ToolController)

router.get(
    "/",
    response_model=CollectionResponse,
    description="get a collection of tools scoped to the current actor",
)(list_tools)
router.post("/", response_model=ToolRead, description="create a new tool")(create_tool)
router.get(
    "/{object_id}", response_model=ToolRead, description="read a single tool by id"
)(read_tool)
router.post(
    "/{object_id}", response_model=ToolRead, description="update a single tool by id"
)(update_tool)
router.put(
    "/{object_id}", response_model=ToolRead, description="update a single tool by id"
)(update_tool)
router.delete(
    "/{object_id}", response_model=None, description="delete a single tool by id"
)(delete_tool)
