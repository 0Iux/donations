from sqlalchemy import select
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


charity_project_crud = CRUDMCharityProject(CharityProject)
