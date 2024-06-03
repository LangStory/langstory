from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.tool import ToolController
from app.routers.utilities import get_db_session, get_current_user, list_router_for_actor_factory
from app.schemas.user_schemas import ScopedUser
from app.schemas.collection_schemas import CollectionResponse

router = APIRouter(prefix="/tools", tags=["tools"])

list_tools = list_router_for_actor_factory(ToolController)

router.get("/", response_model=CollectionResponse)(list_tools)