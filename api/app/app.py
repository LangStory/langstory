from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.v1 import ROUTERS as v1_routes
from app.tags_metadata import TAGS_METADATA # TODO: do this better


def create_app():
    app = FastAPI(
        swagger_ui_parameters={"docExpansion": "none"},
        #openapi_tags=TAGS_METADATA,
        title="☯️ LangStory",
        summary="Create beautiful natural language user experiences.",
        version="0.2.0",  # TODO wire this up to the version in the package
    )
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    for route in v1_routes:
        app.include_router(route, prefix="/v1")
        # this gives undocumented routes for "latest" and bare api calls.
        # we should always tie this to the newest version of the api.
        app.include_router(route, prefix="", include_in_schema=False)
        app.include_router(route, prefix="/latest", include_in_schema=False)
    return app

app = create_app()
