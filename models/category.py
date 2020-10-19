import typing
from pydantic import BaseModel
from pydantic import Field


class Category(BaseModel):
    """Category model."""

    # ID.
    id: typing.Optional[int] = None

    # Name.
    name: str = Field(
        description='Category name',
        max_length=32,
        title='name',
        default=None
    )
