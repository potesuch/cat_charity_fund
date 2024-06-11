from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, CharityProject


async def investment(
        session: AsyncSession
) -> None:
    donations = await session.scalars(
        select(Donation).where(Donation.fully_invested.is_(False))
    )
    projects = await session.scalars(
        select(CharityProject).where(CharityProject.fully_invested.is_(False))
    )
    for project in projects:
        project_amount = project.full_amount - project.invested_amount
        donation = donations.first()
        while not project.fully_invested:
            if donation is None:
                break
            donation_amount = donation.full_amount - donation.invested_amount
            if project_amount > donation_amount:
                project.invested_amount += donation_amount
                donation.invested_amount += donation_amount
                donation.fully_invested = True
            elif project_amount == donation_amount:
                project.invested_amount += donation_amount
                donation.invested_amount += donation_amount
                project.fully_invested = True
                donation.fully_invested = True
            else:
                project.invested_amount += project_amount
                donation.invested_amount += project_amount
                project.fully_invested = True
            if donations.closed:
                break
            donation = donations.first()
        if donations.closed:
            break
    await session.commit()
