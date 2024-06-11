import datetime as dt

from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = None
    model_config = ConfigDict(extra='forbid')

    @field_validator('full_amount')
    @classmethod
    def full_amount_positive(cls, value):
        if value <= 0:
            raise ValueError('Требуемая сумма должна быть больше 0')
        return value

    @field_validator('name', 'description')
    @classmethod
    def name_cannot_be_null(cls, value):
        if value is None or value == '':
            raise ValueError('Поле не может быть пустым!')
        return value


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    full_amount: int


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: dt.datetime
    close_date: Optional[dt.datetime]
