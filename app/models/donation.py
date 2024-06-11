import datetime as dt

from sqlalchemy import (ForeignKey, Text, Integer, Boolean, DateTime,
                        CheckConstraint)
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.core.db import Base


class Donation(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    full_amount: Mapped[int] = mapped_column(Integer)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[dt.datetime] = mapped_column(
        DateTime, default=dt.datetime.now
    )
    close_date: Mapped[dt.datetime] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(full_amount > 0, name='check_full_amount_positive'),
        CheckConstraint(
            invested_amount >= 0, name='check_invested_amount_positive'
        ),
    )

    @validates('fully_invested')
    def validate_fully_invested(self, key, value):
        if value:
            self.close_date = dt.datetime.now()
        return value
