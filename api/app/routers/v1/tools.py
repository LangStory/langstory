from typing import Annotated
from fastapi import APIRouter, File, UploadFile, Depends
import json
from jsonschema import Draft7Validator, validate
from jsonschema.exceptions import SchemaError

from app.models.tool import Tool
from app.controllers.tool import ToolController
from app.routers.utilities import (
    get_current_user,
    get_db_session,
    list_router_for_actor_factory,
    create_router_for_actor_factory,
    read_router_for_actor_factory,
    update_router_for_actor_factory,
    delete_router_for_actor_factory,
)
from app.schemas.tool_schemas import ToolRead, ToolCreate, ToolUpdate
from app.schemas.collection_schemas import CollectionResponse
from app.http_errors import bad_request

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
    "/{tool_id}", response_model=ToolRead, description="read a single tool by id"
)(read_tool)
router.post(
    "/{tool_id}", response_model=ToolRead, description="update a single tool by id"
)(update_tool)
router.put(
    "/{tool_id}", response_model=ToolRead, description="update a single tool by id"
)(update_tool)
router.delete(
    "/{tool_id}", response_model=None, description="delete a single tool by id"
)(delete_tool)

OAI_JSON_SCHEMA = """{
      $schema: "http://json-schema.org/draft/2020-12/schema",
      definitions: {
        objectWithProperties: {
          type: "object",
          properties: {
            type: {
              type: "string",
              enum: [
                "array",
                "boolean",
                "integer",
                "null",
                "number",
                "object",
                "string",
              ],
            },
            name: {
              type: "string",
            },
            description: {
              type: "string",
            },
            parameters: {
              type: "object",
              required: ["type", "required", "properties"],
              properties: {
                type: {
                  type: "string",
                  enum: ["object"],
                },
                required: {
                  type: "array",
                  items: {
                    type: "string",
                  },
                },
                properties: {
                  $ref: "#/definitions/propertiesObject",
                },
              },
              additionalProperties: false,
            },
            enum: {
              type: "array",
              items: {
                type: "string",
              },
            },
            items: {
              oneOf: [
                {
                  $ref: "#/definitions/objectWithProperties",
                },
                {
                  type: "string",
                },
              ],
            },
            required: {
              type: "array",
              items: {
                type: "string",
              },
            },
            properties: {
              $ref: "#/definitions/propertiesObject",
            },
            $ref: {
              type: "string",
            },
          },
          additionalProperties: false,
        },
        propertiesObject: {
          type: "object",
          patternProperties: {
            ".*": {
              $ref: "#/definitions/objectWithProperties",
            },
          },
          additionalProperties: false,
        },
      },
      type: "object",
      required: ["name", "description", "parameters"],
      properties: {
        name: {
          type: "string",
        },
        description: {
          type: "string",
        },
        parameters: {
          type: "object",
          required: ["type", "required", "properties"],
          properties: {
            type: {
              type: "string",
              enum: ["object"],
            },
            required: {
              type: "array",
              items: {
                type: "string",
              },
            },
            properties: {
              $ref: "#/definitions/propertiesObject",
            },
          },
          additionalProperties: false,
        },
      },
      additionalProperties: false,
      }"""

# bulk add from jsonschema file
@router.post("/bulk", description="bulk create tools")
async def bulk_create_tools(
    project_id: str,
    tools: UploadFile,
    db_session = Depends(get_db_session),
    actor = Depends(get_current_user)) -> CollectionResponse:
    pass
    tools_body = await tools.read()
    schemas = json.loads(tools_body.decode("utf-8"))

    try:
        # check that each schema is valid
        _ = [Draft7Validator.check_schema(schema) for schema in schemas]
        validate(schemas, json.loads(OAI_JSON_SCHEMA))

    except SchemaError as e:
        bad_request(e, e.message)

    # loop through and create each tool
    tools = []
    for schema in schemas:
        tool = Tool(
            name=schema["name"],
            description=schema["description"],
            json_schema=tool,
            project_id=project_id)
        tools.append(tool)
        db_session.add(tool)
    db_session.commit()
    return CollectionResponse(data=[ToolRead.model_validate(tool) for tool in tools])