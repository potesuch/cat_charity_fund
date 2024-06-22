import datetime as dt

from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CharityProjectBase(BaseModel):
    """
    Базовая модель благотворительного проекта.

    Attributes:
        name (Optional[str]): Имя проекта.
        description (Optional[str]): Описание проекта.
        full_amount (Optional[int]): Сумма, необходимая для полного финансирования проекта.
    """
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
    """
    Модель для обновления благотворительного проекта.
    """
    pass


class CharityProjectCreate(CharityProjectBase):
    """
    Модель для создания благотворительного проекта.

    Attributes:
        name (str): Имя проекта.
        description (str): Описание проекта.
        full_amount (int): Сумма, необходимая для полного финансирования проекта.
    """
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    full_amount: int


class CharityProjectDB(CharityProjectCreate):
    """
    Модель благотворительного проекта в базе данных.

    Attributes:
        id (int): Идентификатор благотворительного проекта.
        invested_amount (int): Сумма, уже вложенная в проект.
        fully_invested (bool): Флаг, указывающий, полностью ли профинансирован проект.
        create_date (dt.datetime): Дата создания проекта.
        close_date (dt.datetime): Дата закрытия проекта (если применимо).
    """
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: dt.datetime
    close_date: Optional[dt.datetime]
