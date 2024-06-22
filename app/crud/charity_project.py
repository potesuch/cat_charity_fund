from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, User
from app.schemas.charity_project import (CharityProjectCreate,
                                        CharityProjectUpdate)
from app.services.investment import investment


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):
    """
    Класс для операций CRUD с моделью CharityProject.
    """

    async def create(
        self,
        obj_in: CharityProjectCreate,
        session: AsyncSession,
        user: Optional[User] = None
    ) -> CharityProject:
        """
        Создает новый благотворительный проект и запускает инвестиционный процесс.

        Args:
            obj_in (CharityProjectCreate): Данные для создания проекта.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            user (Optional[User]): Пользователь, создающий проект (если применимо).

        Returns:
            CharityProject: Созданный проект.
        """
        project = await super().create(obj_in, session)
        await investment(session)
        await session.refresh(project)
        return project

    async def get_id_by_name(
        self,
        name: str,
        session: AsyncSession
    ) -> Optional[int]:
        """
        Получает ID проекта по его имени.

        Args:
            name (str): Имя проекта.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            Optional[int]: ID проекта или None, если проект не найден.
        """
        project_id = await session.scalar(
            select(CharityProject.id).where(CharityProject.name == name)
        )
        return project_id


charityproject_crud = CRUDCharityProject(CharityProject)
