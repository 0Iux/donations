from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDMCharityProject(CRUDBase):
    async def get_project_by_name(
            self,
            name: str,
            session: AsyncSession
    ) -> CharityProject:
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == name,
            )
        )
        project = project.scalars().first()
        return project

    async def get_all_closed_projects(
            self,
            session: AsyncSession
    ) -> list[CharityProject]:
        charity_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(
                func.julianday(CharityProject.close_date) -
                func.julianday(CharityProject.create_date)
            )
        )
        return charity_projects.scalars().all()


charity_project_crud = CRUDMCharityProject(CharityProject)
