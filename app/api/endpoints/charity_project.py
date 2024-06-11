from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charity_project import (CharityProjectDB,
                                         CharityProjectCreate,
                                         CharityProjectUpdate)
from app.core.db import get_async_session
from app.crud.charity_project import charityproject_crud
from app.api.validators import (check_name_duplicate,
                                check_project_before_delete,
                                check_project_before_edit)
from app.core.user import current_superuser

router = APIRouter(prefix='/charity_project', tags=['charity_projects'])


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получает список всех проектов.
    """
    projects = await charityproject_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Создает благотворительный проект.
    """
    await check_name_duplicate(project.name, session)
    new_project = await charityproject_crud.create(project, session)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы
     средства, его можно только закрыть.
    """
    project = await check_project_before_delete(project_id, session)
    project = await charityproject_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать, также нельзя установить требуемую
     сумму меньше уже вложенной.

    """
    project = await check_project_before_edit(
        project_id, project_in.full_amount, session
    )
    if project_in.name is not None:
        await check_name_duplicate(project_in.name, session)
    updated_project = await charityproject_crud.update(
        project_in, project, session
    )
    return updated_project
