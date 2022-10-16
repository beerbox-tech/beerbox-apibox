"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

unit testing beerbox api response
"""

from beerbox.application.api.components.base import APIComponent
from beerbox.application.api.response import APIResponse


class Dummy(APIComponent):
    """dummy component to test rendering"""

    dummy: bool


def test_render__single():
    """test the response rendering with a single component"""
    response = APIResponse(content=Dummy(dummy=True), status_code=418)
    assert response.body == b'{"dummy":true}'


def test_render__list():
    """test the response rendering with a single component"""
    response = APIResponse(content=[Dummy(dummy=True), Dummy(dummy=False)], status_code=418)
    assert response.body == b'[{"dummy":true},{"dummy":false}]'
