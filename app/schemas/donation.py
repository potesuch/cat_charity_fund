import datetime as dt
from typing import Optional

from pydantic import BaseModel, field_validator


class DonationBase(BaseModel):
    """
    Базовая модель для пожертвования.

    Attributes:
        full_amount (int): Сумма пожертвования.
        comment (Optional[str]): Комментарий к пожертвованию.
    """
    full_amount: int
    comment: Optional[str] = None

    @field_validator('full_amount')
    @classmethod
    def full_amount_positive(csl, value):
        if value <= 0:
            raise ValueError('Сумма пожертвования должна быть больше 0')
        return value


class DonationCreate(DonationBase):
    """
    Модель для создания пожертвования.
    """
    pass


class DonationDBShort(DonationBase):
    """
    Короткая модель пожертвования в базе данных.

    Attributes:
        full_amount (int): Сумма пожертвования.
        comment (Optional[str]): Комментарий к пожертвованию.
        id (int): Идентификатор пожертвования.
        create_date (dt.datetime): Дата создания пожертвования.
    """
    full_amount: int
    comment: Optional[str]
    id: int
    create_date: dt.datetime


class DonationDB(DonationDBShort):
    """
    Модель пожертвования в базе данных.

    Attributes:
        user_id (int): ID пользователя, сделавшего пожертвование.
        invested_amount (int): Сумма, вложенная из пожертвования.
        fully_invested (bool): Флаг, указывающий, полностью ли вложено пожертвование.
        close_date (Optional[dt.datetime]): Дата закрытия пожертвования (если применимо).
    """
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[dt.datetime]
