import pytest
from fastapi import Request
from fastapi import HTTPException

from starlette.datastructures import Headers

from controller import check_auth


def test_check_auth_error_key_is_not_set():
    """Test: check_auth(request: Request) -> None
    Error: Key is not set."""

    scope = {'type': 'http'}
    request = Request(scope)
    request._headers = []
    with pytest.raises(HTTPException) as ex:
        check_auth(request)
    assert ex.value.status_code == 400
    assert ex.value.detail == 'Key is not set'


def test_check_auth_error_auth_error():
    """Test: check_auth(request: Request) -> None
    Error: Auth error."""

    scope = {'type': 'http'}
    request = Request(scope)
    request._headers = Headers(headers={'X-Key': 'fake-key'})
    with pytest.raises(HTTPException) as ex:
        check_auth(request)
    assert ex.value.status_code == 400
    assert ex.value.detail == 'Auth error'
