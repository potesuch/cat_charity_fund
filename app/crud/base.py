from typing import TypeVar, Generic, Type, Optional, Sequence

from fastapi.encoders import jsonable_encoder

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс для операций CRUD.

    Attributes:
        model (Type[ModelType]): Модель базы данных.
    """

    def __init__(
            self,
            model: Type[ModelType]
    ):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        """
        Получает объект по ID.

        Args:
            obj_id (int): ID объекта.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            Optional[ModelType]: Найденный объект или None.
        """
        db_obj = await session.get(self.model, obj_id)
        return db_obj

    async def get_multi(
            self,
            session: AsyncSession
    ) -> Sequence[ModelType]:
        """
        Получает все объекты.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            Sequence[ModelType]: Список объектов.
        """
        db_objs = await session.scalars(select(self.model))
        return db_objs.all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> ModelType:
        """
        Создает новый объект.

        Args:
            obj_in (CreateSchemaType): Данные для создания объекта.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            user (Optional[User]): Пользователь, создающий объект (если применимо).

        Returns:
            ModelType: Созданный объект.
        """
        obj_in_data = obj_in.model_dump()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            obj_in: UpdateSchemaType,
            db_obj: ModelType,
            session: AsyncSession
    ) -> ModelType:
        """
        Обновляет существующий объект.

        Args:
            obj_in (UpdateSchemaType): Данные для обновления объекта.
            db_obj (ModelType): Существующий объект.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            ModelType: Обновленный объект.
        """
        db_obj_data = jsonable_encoder(db_obj)
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        for field in db_obj_data:
            if field in obj_in_data:
                setattr(db_obj, field, obj_in_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession
    ) -> ModelType:
        """
        Удаляет объект.

        Args:
            db_obj (ModelType): Объект для удаления.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            ModelType: Удаленный объект.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj
