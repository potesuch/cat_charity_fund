import datetime as dt

from sqlalchemy import (String, Text, Boolean, Integer, DateTime,
                        CheckConstraint)
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.core.db import Base


class CharityProject(Base):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text)
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
