from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.api.validators import (
    check_charity_project_id_exists,
    check_new_full_amount_more,
    check_no_invested_amount,
    check_unique_name,
    check_project_full_invested
)
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate
)
from app.crud.charity_project import charity_project_crud
from app.core.user import current_superuser

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def post_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_unique_name(charity_project.name, session)
    project = await charity_project_crud.create(charity_project, session)
    return await charity_project_crud.invest(project, session)


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_id_exists(
        charity_project_id,
        session
    )
    await check_no_invested_amount(charity_project_id, session)
    return await charity_project_crud.remove(charity_project, session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_id_exists(
        charity_project_id, session
    )
    await check_project_full_invested(charity_project_id, session)
    if obj_in.name is not None:
        await check_unique_name(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_new_full_amount_more(
            charity_project_id, session, obj_in.full_amount
        )
        if obj_in.full_amount == charity_project.invested_amount:
            charity_project = await charity_project_crud.close_obj(charity_project)
    return await charity_project_crud.update(charity_project, obj_in, session)
