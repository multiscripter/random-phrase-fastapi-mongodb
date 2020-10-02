from settings import settings
settings['db_name'] = 'phrase-fastapi-mongodb-test'

import pytest
from datetime import datetime
from models.phrase import Phrase
from pymongo import MongoClient
from starlette.testclient import TestClient
import re
from main import app

# https://www.jetbrains.com/help/pycharm/pytest.html#create-pytest-test

# Запуск тестов с покрытием из корня проекта.
# coverage erase
# coverage run -m pytest -p no:cacheprovider ./tests/*
# coverage html


client = MongoClient()
db = client[settings['db_name']]
collection = db[settings['cln_name']]
req_client = TestClient(app)


@pytest.fixture(autouse=True)
def run_around_tests():
    # Actions before each test.
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
    collection.delete_many({})


def test_get_list_success():
    """Test: Method GET, URI /phrases/"""

    expected = []
    for found in collection.find():
        phrase = Phrase(**found)
        phrase.date = phrase.date.isoformat()
        expected.append(phrase)

    response = req_client.get('http://127.0.0.1:8000/phrases/')
    assert response.status_code == 200

    actual = response.json()
    assert expected == actual


def test_create_success():
    """Test: Method POST, URI /phrases/"""

    id = collection.count_documents({}) + 1
    data = {
        'author': 'create-author',
        'text': 'created-text'
    }
    expected = Phrase(**data, date=datetime.utcnow())
    expected.id = id

    response = req_client.post('http://127.0.0.1:8000/phrases/', json=data)
    assert response.status_code == 201

    actual = response.json()
    assert expected.id == actual['id']
    assert expected.author == actual['author']
    assert expected.text == actual['text']
    assert re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', actual['date'])


def test_delete_success():
    """Test: Method DELETE, URI /phrases/"""

    id = 2
    response = req_client.delete(f'http://127.0.0.1:8000/phrases/{id}/')
    assert response.status_code == 200

    actual = response.json()
    assert 1 == actual
    assert 1 == collection.count_documents({})


def test_update_success():
    """Test: Method PATCH, URI /phrases/{id}/"""

    id = 2
    data = {
        'author': 'updated author',
        'text': 'updated text'
    }
    response = req_client.patch(f'http://127.0.0.1:8000/phrases/{id}/', json=data)
    assert response.status_code == 205

    actual = response.json()
    assert 1 == actual

    actual = collection.find_one({'id': id})
    assert data['author'] == actual['author']
    assert data['text'] == actual['text']
