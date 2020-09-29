from dao.phrase_repository import PhraseRepository
from fastapi import APIRouter
from models.phrase import Phrase
from settings import settings
from typing import List

router = APIRouter()


@router.get(
    '/',
    description='Get a list of all phrases',
    response_description='List of phrases',
    response_model=List[Phrase],
    status_code=200
)
async def get_list() -> List[Phrase]:
    return get_repository().get()


@router.post(
    '/',
    description='Create new phrase',
    response_description='Created phrase',
    response_model=Phrase,
    status_code=201
)
async def create(data: dict = None) -> Phrase:
    return get_repository().create(data)


@router.delete(
    '/',
    description='Delete phrase',
    response_description='Affected entries',
    status_code=200
)
async def delete(data: dict = None) -> int:
    return get_repository().delete(data)


@router.patch(
    '/{id}/',
    description='Update phrase',
    response_description='Updated entries',
    status_code=205
)
async def update(id: int, data: dict) -> int:
    return get_repository().update(id, data)


def get_repository():
    return PhraseRepository(
        settings['db_name'],
        settings['cln_name']
    )
