"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

unit testing apibox api exception handlers
"""

import json
from unittest.mock import Mock

import pytest
from fastapi.exceptions import RequestValidationError
from psycopg2 import OperationalError as PostgresOperationalError
from pydantic import BaseModel
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from sqlalchemy.exc import OperationalError
from starlette.exceptions import HTTPException

from apibox.application.api.exception_handlers import exception_handler
from apibox.domain.contributions import ContributionDoesNotExist
from apibox.domain.contributions import ContributionUserDoesNotExist
from apibox.domain.users import UserAlreadyExist
from apibox.domain.users import UserDoesNotExist


def mock_request(url: str) -> Mock:
    """create a mock request"""
    mock = Mock()
    mock.url.path = url
    return mock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code, code, message",
    (
        (400, "bad-request", "bad request"),
        (401, "unauthorized", "unauthorized"),
        (402, "payment-required", "payment required"),
        (403, "forbidden", "forbidden"),
        (404, "not-found", "requested path does not exist"),
        (405, "method-not-allowed", "method not allowed"),
        (406, "not-acceptable", "not acceptable"),
        (407, "proxy-authentication-required", "proxy authentication required"),
        (408, "request-timeout", "request timeout"),
        (409, "conflict", "conflict"),
        (410, "gone", "gone"),
        (411, "length-required", "length required"),
        (412, "precondition-failed", "precondition failed"),
        (413, "request-entity-too-large", "request entity too large"),
        (414, "request-uri-too-long", "request-uri too long"),
        (415, "unsupported-media-type", "unsupported media type"),
        (416, "requested-range-not-satisfiable", "requested range not satisfiable"),
        (417, "expectation-failed", "expectation failed"),
        (418, "i-am-a-teapot", "i'm a teapot"),
        (421, "misdirected-request", "misdirected request"),
        (422, "unprocessable-entity", "unprocessable entity"),
        (423, "locked", "locked"),
        (424, "failed-dependency", "failed dependency"),
        (425, "too-early", "too early"),
        (426, "upgrade-required", "upgrade required"),
        (428, "precondition-required", "precondition required"),
        (429, "too-many-requests", "too many requests"),
        (431, "request-header-fields-too-large", "request header fields too large"),
        (451, "unavailable-for-legal-reasons", "unavailable for legal reasons"),
        (500, "internal-server-error", "internal server error"),
        (501, "not-implemented", "not implemented"),
        (502, "bad-gateway", "bad gateway"),
        (503, "service-unavailable", "service unavailable"),
        (504, "gateway-timeout", "gateway timeout"),
        (505, "http-version-not-supported", "http version not supported"),
        (506, "variant-also-negotiates", "variant also negotiates"),
        (507, "insufficient-storage", "insufficient storage"),
        (508, "loop-detected", "loop detected"),
        (510, "not-extended", "not extended"),
        (511, "network-authentication-required", "network authentication required"),
    ),
)
async def test_http_exception_handler(status_code: int, code: str, message: str):
    """test exception_handler for all HTTPException"""
    request = mock_request("/test")
    response = await exception_handler(request, HTTPException(status_code=status_code))

    assert response.status_code == status_code
    assert json.loads(response.body) == {"code": code, "message": message}


@pytest.mark.asyncio
async def test_database_exception_handler():
    """test exception_handler for SQLAlchemyError"""
    request = mock_request("/test")
    exception = OperationalError(
        params=None,
        statement=None,
        orig=PostgresOperationalError(
            'connection to server at "localhost" (::1), port 5432 failed: Connection refused\n\t'
            "Is the server running on that host and accepting TCP/IP connections?\n"
            'connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused'
            "Is the server running on that host and accepting TCP/IP connections?\n",
        ),
    )

    response = await exception_handler(request, exception)

    assert response.status_code == 500
    assert json.loads(response.body) == {
        "code": "database-error",
        "data": {"code": "e3q8", "type": "operational-error"},
        "message": (
            '(psycopg2.operationalerror) connection to server at "localhost" '
            "(::1), port 5432 failed: connection refused"
        ),
    }


@pytest.mark.asyncio
async def test_validation_exception_handler():
    """test exception_handler for SQLAlchemyError"""
    request = mock_request("/test")
    item_error = ErrorWrapper(exc=ValueError("something went wrong"), loc="field")
    item_exc = ValidationError(errors=[item_error], model=BaseModel)
    body_error = ErrorWrapper(exc=item_exc, loc=("items", 1))
    body_exc = ValidationError(errors=[body_error], model=BaseModel)
    exception = RequestValidationError(errors=[ErrorWrapper(exc=body_exc, loc="body")])

    response = await exception_handler(request, exception)

    assert response.status_code == 422
    assert json.loads(response.body) == {
        "code": "validation-error",
        "data": [{"field": "body.items[1].field", "message": "something went wrong"}],
        "message": "error validating input data",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception, status_code, code, message, data",
    (
        (
            UserDoesNotExist("public-id"),
            404,
            "user-not-found",
            "the requested user does not exist",
            None,
        ),
        (
            UserAlreadyExist("username"),
            409,
            "user-conflict",
            "a user with the same username already exist",
            None,
        ),
        (
            ContributionDoesNotExist("public-id"),
            404,
            "contribution-not-found",
            "the requested contribution does not exist",
            None,
        ),
        (
            ContributionUserDoesNotExist("public-id"),
            422,
            "validation-error",
            "error creating contribution",
            [{"field": "body.userId", "message": "requested user does not exist"}],
        ),
    ),
)
async def test_custom_exception_handler(exception, status_code, code, message, data):
    """test exception_handler for custom errors"""
    request = mock_request("/test")

    response = await exception_handler(request, exception)

    assert response.status_code == status_code
    if data:
        assert json.loads(response.body) == {"code": code, "message": message, "data": data}
    else:
        assert json.loads(response.body) == {"code": code, "message": message}


@pytest.mark.asyncio
async def test_exception_handler():
    """test exception_handler for python Exception"""
    request = mock_request("/test")
    exception = ValueError()

    response = await exception_handler(request, exception)

    assert response.status_code == 500
    assert json.loads(response.body) == {
        "code": "internal-error",
        "message": "unknown error",
    }
