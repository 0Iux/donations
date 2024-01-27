from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDMDonations(CRUDBase):
    async def get_all_user_donations(
            self,
            user: User,
            session: AsyncSession,
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id,
            )
        )
        return donations.scalars().all()


donations_crud = CRUDMDonations(Donation)
