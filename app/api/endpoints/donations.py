from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import User
from app.schemas.donations import (
    DonationBase,
    DonationDB,
    AllDonations, DonationCreate
)
from app.crud.donations import donations_crud
from app.core.user import current_user

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
):
    return await donations_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[AllDonations],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_all_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donations_crud.get_all_user_donations(user, session)


@router.post(
    '/',
    response_model=DonationCreate,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def post_donation(
    donation: DonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donation = await donations_crud.create(donation, session, user)
    return await donations_crud.invest(donation, session)
