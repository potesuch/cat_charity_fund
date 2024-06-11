from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate
from app.services.investment import investment


class CRUDDonation(CRUDBase[
    Donation,
    DonationCreate,
    BaseModel
]):

    async def create(
            self,
            obj_in: DonationCreate,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> Donation:
        donation = await super().create(obj_in, session, user)
        await investment(session)
        await session.refresh(donation)
        return donation

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> Sequence[Donation]:
        donations = await session.scalars(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.all()


donation_crud = CRUDDonation(Donation)
