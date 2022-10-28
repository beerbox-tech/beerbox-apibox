"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox api exception handlers
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException

from beerbox.application.api.exception_handlers import exception_handler
from beerbox.application.api.resources import contributions
from beerbox.application.api.resources import health
from beerbox.application.api.resources import users


def create_app() -> FastAPI:
    """create a fastapi application"""
    app = FastAPI(openapi_url="")

    # routers to expose endpoints
    for router in (health.router, users.router, contributions.router):
        app.include_router(router)

    # exception handlers to manage errors
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
