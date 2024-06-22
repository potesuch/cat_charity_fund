from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    """
    Проверяет, существует ли проект с указанным именем.

    Args:
        project_name (str): Имя проекта для проверки.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Raises:
        HTTPException: Если проект с таким именем уже существует.
    """
    project_id = await charityproject_crud.get_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_charityproject_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    """
    Проверяет, существует ли проект с указанным идентификатором.

    Args:
        project_id (int): Идентификатор проекта для проверки.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        CharityProject: Найденный проект.

    Raises:
        HTTPException: Если проект не найден.
    """
    project = await charityproject_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_project_before_delete(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    """
    Проверяет, можно ли удалить проект с указанным идентификатором.

    Args:
        project_id (int): Идентификатор проекта для проверки.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        CharityProject: Найденный проект.

    Raises:
        HTTPException: Если проект полностью или частично инвестирован и не подлежит удалению.
    """
    project = await check_charityproject_exists(project_id, session)
    if project.fully_invested or project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_project_before_edit(
    project_id: int,
    project_full_amount,
    session: AsyncSession
) -> CharityProject:
    """
    Проверяет, можно ли редактировать проект с указанным идентификатором.

    Args:
        project_id (int): Идентификатор проекта для проверки.
        project_full_amount: Полная сумма проекта для проверки.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        CharityProject: Найденный проект.

    Raises:
        HTTPException: Если проект закрыт или если требуемая сумма меньше текущей.
    """
    project = await check_charityproject_exists(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    if project_full_amount is not None:
        if project_full_amount < project.invested_amount:
            raise HTTPException(
                status_code=422,
                detail='Нельзя установить требуемую сумму меньше внесенной'
            )
        elif project_full_amount == project.invested_amount:
            project.fully_invested = True
    return project
