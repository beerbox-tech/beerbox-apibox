"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

apibox api exception handlers
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException

from apibox.application.api.exception_handlers import exception_handler
from apibox.application.api.resources import boxes
from apibox.application.api.resources import contributions
from apibox.application.api.resources import health
from apibox.application.api.resources import users


def create_app() -> FastAPI:
    """create a fastapi application"""
    app = FastAPI(openapi_url="")

    # routers to expose endpoints
    for resource in (health, users, contributions, boxes):
        app.include_router(resource.router)

    # exception handlers to manage errors
    # custom exception are handled by the generic exception handler
    for exception in (SQLAlchemyError, HTTPException, Exception, RequestValidationError):
        app.add_exception_handler(exception, exception_handler)

    # cors configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
