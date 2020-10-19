import typing
from datetime import datetime
from pydantic import BaseModel
from pydantic import Field
from models.category import Category


class Phrase(BaseModel):
    """Phrase model."""

    def __init__(self, **data: typing.Any):
        super().__init__(**data)
        if 'category' in data:
            self.category = Category(**data['category'])

    # ID.
    id: typing.Optional[int] = None

    # Phrase author.
    author: str = Field(
        description='Phrase author',
        max_length=64,
        title='author'
    )

    category: Category = {}

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
