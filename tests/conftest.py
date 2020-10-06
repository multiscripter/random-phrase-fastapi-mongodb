from settings import settings

settings['db_name'] = 'phrase-fastapi-mongodb-test'

import pytest


@pytest.hookimpl()
def pytest_sessionstart(session):
    """Actions before all tests."""


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    """Actions after all tests."""
