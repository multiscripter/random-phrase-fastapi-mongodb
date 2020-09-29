from settings import settings
settings['db_name'] = 'phrase-fastapi-mongodb-test'

from datetime import datetime
from pymongo import MongoClient
import pytest


@pytest.hookimpl()
def pytest_sessionstart(session):
    """Actions before all tests."""

    client = MongoClient()
    db = client[settings['db_name']]
    collection = db[settings['cln_name']]
    phrases = []
    for a in range(1, 3):
        phrases.append({
            'id': a,
            'author': f'test-author-{a}',
            'text': f'test-text-{a}',
            'date': datetime.utcnow()
        })
    collection.insert_many(phrases)


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    """Actions after all tests."""

    client = MongoClient()
    db = client[settings['db_name']]
    collection = db[settings['cln_name']]
    collection.delete_many({})
