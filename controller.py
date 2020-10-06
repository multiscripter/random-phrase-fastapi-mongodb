from fastapi import APIRouter
from fastapi import Request
from typing import List
from services.phraseService import PhraseService
from models.phrase import Phrase
from settings import settings

router = APIRouter()

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
async def create(data: dict = None) -> Phrase:
    return get_service().create(data)


@router.delete(
    '/{id}/',
    description='Delete phrase',
    response_description='Affected entries',
    status_code=200
)
async def delete(id: int) -> int:
    return get_service().delete(id)


@router.patch(
    '/{id}/',
    description='Update phrase',
    response_description='Updated entries',
    status_code=205
)
async def update(id: int, data: dict) -> int:
    return get_service().update(id, data)


def get_service():
    return PhraseService(
        settings['db_name'],
        settings['cln_name']
    )
