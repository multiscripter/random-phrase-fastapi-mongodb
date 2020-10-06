from settings import settings
settings['db_name'] = 'phrase-fastapi-mongodb-test'

import pytest
from datetime import datetime
from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import DeleteResult
from pymongo.results import InsertOneResult
from pymongo.results import UpdateResult
from starlette.datastructures import QueryParams
from services.phraseService import PhraseService

# https://www.jetbrains.com/help/pycharm/pytest.html#create-pytest-test

# Запуск тестов с покрытием из корня проекта.
# coverage erase
# coverage run -m pytest -p no:cacheprovider ./tests/*
# coverage html


@pytest.fixture(autouse=True)
def run_around_tests():
    # Actions before each test.
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

    yield # run test.

    # Actions after each test.
    client = MongoClient()
    db = client[settings['db_name']]
    collection = db[settings['cln_name']]
    collection.delete_many({})


def test_get_random_phrase():
    """Test: get(self, params: QueryParams = None) -> List[Phrase]
    Random phrase."""

    service = PhraseService(
        settings['db_name'],
        settings['cln_name']
    )
    params = QueryParams({
        'random': ''
    })
    result = service.get(params)
    assert 1 == len(result)
    assert result[0].author.startswith('test-author-')


def test_get_random_phrase_less_one():
    """Test: get(self, params: QueryParams = None) -> List[Phrase]
    Random phrase. Query param less then 1"""

    service = PhraseService(
        settings['db_name'],
        settings['cln_name']
    )
    params = QueryParams({
        'random': 0
    })
    result = service.get(params)
    assert 1 == len(result)
    assert result[0].author.startswith('test-author-')


def test_get_phrases_by_author():
    """Test: get(self, params: QueryParams = None) -> List[Phrase]
    Returns list of phrases by author."""

    service = PhraseService(
        settings['db_name'],
        settings['cln_name']
    )
    service.create(data = {
        'author': 'test-author-1',
        'text': 'test-text-2'
    })
    params = QueryParams({
        'author': 'test-author-1'
    })
    result = service.get(params)
    assert 2 == len(result)


def test_get_phrases_by_id():
    """Test: get(self, params: QueryParams = None) -> List[Phrase]
    Returns list of phrases by id."""

    service = PhraseService(
        settings['db_name'],
        settings['cln_name']
    )
    params = QueryParams({
        'id': '1'
    })
    result = service.get(params)
    assert 1 == len(result)
    assert result[0].author.startswith('test-author-1')


def test_create_http_exception(mocker):
    """Test: create(self, data: dict) -> int
    HTTPException: Creation error."""

    service = PhraseService(
        settings['db_name'],
        settings['cln_name']
    )
    insert_result = InsertOneResult(0, None)
    mock_insert_one = mocker.patch.object(Collection, 'insert_one')
    mock_insert_one.return_value = insert_result
    service.collection.insert_one = mock_insert_one

    data = {
        'author': 'create-author',
        'text': 'created-text'
    }
    with pytest.raises(HTTPException) as ex:
        service.create(data)

    assert 400 == ex.value.status_code
    assert 'Creation error' == ex.value.detail


def test_delete_http_exception(mocker):
    """Test: delete(self, id: int) -> int
    HTTPException: Deletion error."""

    service = PhraseService(
        settings['db_name'],
        settings['cln_name']
    )
    delete_result = DeleteResult(None, False)
    mock_delete_many = mocker.patch.object(Collection, 'delete_many')
    mock_delete_many.return_value = delete_result
    service.collection.delete_many = mock_delete_many

    with pytest.raises(HTTPException) as ex:
        service.delete(1)

    assert 400 == ex.value.status_code
    assert 'Deletion error' == ex.value.detail


def test_update_http_exception(mocker):
    """Test: update(self, id: int, data: dict) -> int
    HTTPException: Update error."""

    service = PhraseService(
        settings['db_name'],
        settings['cln_name']
    )
    update_result = UpdateResult(None, False)
    mock_update_one = mocker.patch.object(Collection, 'update_one')
    mock_update_one.return_value = update_result
    service.collection.update_one = mock_update_one

    with pytest.raises(HTTPException) as ex:
        service.update(1, {'status': 1})

    assert 400 == ex.value.status_code
    assert 'Update error' == ex.value.detail
