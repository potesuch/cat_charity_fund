import datetime as dt
from typing import Optional

from pydantic import BaseModel, field_validator


class DonationBase(BaseModel):
    full_amount: int
    comment: Optional[str] = None

    @field_validator('full_amount')
    @classmethod
    def full_amount_positive(csl, value):
        if value <= 0:
            raise ValueError('Сумма пожертвования должна быть больше 0')
        return value


class DonationCreate(DonationBase):
    pass


class DonationDBShort(DonationBase):
    full_amount: int
    comment: Optional[str]
    id: int
    create_date: dt.datetime


class DonationDB(DonationDBShort):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[dt.datetime]
