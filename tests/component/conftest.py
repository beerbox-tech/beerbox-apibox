"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

apibox component tests configuration
"""

import pytest


def pytest_addoption(parser):
    """inject parameters to pytest cli"""
    parser.addoption("--port", action="store")
    parser.addoption("--host", action="store")


@pytest.fixture(scope="session")
def host(request):
    """expose a host fixture"""
    _host = request.config.option.host
    if not _host:
        return "localhost"
    return _host


@pytest.fixture(scope="session")
def port(request):
    """expose a port fixture"""
    _port = request.config.option.port
    if not _port:
        return 8000
    return _port
