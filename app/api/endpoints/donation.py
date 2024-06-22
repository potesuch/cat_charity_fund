from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.donation import DonationDB, DonationCreate, DonationDBShort
from app.core.user import current_superuser, current_user
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.models import User

router = APIRouter(prefix='/donation', tags=['donations'])


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Получиает все пожертвования.
    """
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationDBShort,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Создает новое пожертвование.
    """
    new_donation = await donation_crud.create(donation, session, user)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationDBShort],
    response_model_exclude_none=True
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Получиает все пожертвования текущего пользователя.
    """
    donations = await donation_crud.get_by_user(session, user)
    return donations
