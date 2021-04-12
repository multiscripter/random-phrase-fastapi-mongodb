import os
from fastapi import APIRouter, HTTPException
from fastapi import Request
from typing import List

from services.authService import AuthService
from services.phraseService import PhraseService
from models.phrase import Phrase
from settings import settings

root_dir = os.path.abspath(__file__).split('controller.py')[0]
router = APIRouter()


# Can get phrase list by any models field:
# http://127.0.0.1:8000/phrases/?id=59
# http://127.0.0.1:8000/phrases/?category.id=1
@router.get(
    '/',
    description='Get a list of all phrases',
    response_description='List of phrases',
    response_model=List[Phrase],
    status_code=200
)
async def get_list(request: Request) -> List[Phrase]:
    return get_service().get(request.query_params)


@router.post(
    '/',
    description='Create new phrase',
    response_description='Created phrase',
    response_model=Phrase,
    status_code=201
)
async def create(request: Request, data: dict = None) -> Phrase:
    check_auth(request)
    return get_service().create(data)


@router.delete(
    '/{id}/',
    description='Delete phrase',
    response_description='Affected entries',
    status_code=200
)
async def delete(request: Request, id: int) -> int:
    check_auth(request)
    return get_service().delete(id)


@router.patch(
    '/{id}/',
    description='Update phrase',
    response_description='Updated entries',
    status_code=205
)
async def update(request: Request, id: int, data: dict) -> int:
    check_auth(request)
    return get_service().update(id, data)


def check_auth(request: Request) -> None:
    auth = AuthService(root_dir)
    if 'x-key' not in request.headers:
        raise HTTPException(400, 'Key is not set')
    elif not auth.check(request.headers['x-key']):
        raise HTTPException(400, 'Auth error')


def get_service():
    return PhraseService(
        settings['db_name'],
        settings['cln_name']
    )
