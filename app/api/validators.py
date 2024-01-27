from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def check_charity_project_id_exists(
        charity_project_id: int,
        session: AsyncSession
):
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_unique_name(
        charity_project_name: str,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get_project_by_name(
        charity_project_name,
        session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_no_invested_amount(
        charity_project_id: int,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_new_full_amount_more(
        charity_project_id: int,
        session: AsyncSession,
        full_amount: int
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if charity_project.invested_amount > full_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Новая требуемая сумма меньше уже накопившейся'
        )


async def check_project_full_invested(
        charity_project_id: int,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
