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

    async def create(
        self,
        obj_in: CharityProjectCreate,
        session: AsyncSession,
        user: Optional[User] = None
    ) -> CharityProject:
        project = await super().create(obj_in, session)
        await investment(session)
        await session.refresh(project)
        return project

    async def get_id_by_name(
        self,
        name: str,
        session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.scalar(
            select(CharityProject.id).where(CharityProject.name == name)
        )
        return project_id


charityproject_crud = CRUDCharityProject(CharityProject)
