from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            declared_attr)

from app.core.config import settings


class Base(DeclarativeBase):
    """
    Базовый класс для моделей SQLAlchemy.

    Attributes:
        id (Mapped[int]): Первичный ключ.
    """
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls):
        """
        Метод, возвращающий название таблицы, основанное на имени класса.
        """
        return cls.__name__.lower()


engine = create_async_engine(settings.database_url, echo=True)

async_session = async_sessionmaker(engine)


async def get_async_session():
    """
    Асинхронный генератор, предоставляющий сессию для работы с базой данных.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    async with async_session() as session:
        yield session
