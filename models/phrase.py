import typing
from datetime import datetime
from pydantic import BaseModel
from pydantic import Field


class Phrase(BaseModel):
    """Phrase model."""

    # ID.
    id: typing.Optional[int] = None

    # Phrase author.
    author: str = Field(
        description='Phrase author',
        max_length=64,
        title='author'
    )

    # Text of phrase.
    text: str = Field(
        description='Text of phrase',
        max_length=256,
        title='Text'
    )

    # Date of creation.
    date: datetime = Field(
        description='Date of creation',
        title='Created'
    )
