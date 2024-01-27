from datetime import datetime
from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation, User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def close_obj(
            self,
            obj: Union[Donation, CharityProject],
    ):
        obj.fully_invested = True
        obj.invested_amount = obj.full_amount
        obj.close_date = datetime.now()
        return obj

    async def invest(
            self,
            obj_in: Union[Donation, CharityProject],
            session: AsyncSession,
    ):
        if isinstance(obj_in, Donation):
            obj_class = CharityProject
        else:
            obj_class = Donation
        objs_db = await session.execute(
            select(obj_class).where(
                obj_class.fully_invested == 0
            ).order_by(
                obj_class.id.desc()
            )
        )
        objs_db = objs_db.scalars().all()
        while objs_db and obj_in.full_amount > obj_in.invested_amount:
            obj_db = objs_db.pop()
            need = obj_db.full_amount - obj_db.invested_amount
            have = obj_in.full_amount - obj_in.invested_amount

            if need > have:
                obj_in = await self.close_obj(obj_in)
                obj_db.invested_amount += have
            elif need == have:
                obj_in = await self.close_obj(obj_in)
                obj_db = await self.close_obj(obj_db)
            else:
                obj_db = await self.close_obj(obj_db)
                obj_in.invested_amount += need
            session.add(obj_db)
        session.add(obj_in)
        await session.commit()
        await session.refresh(obj_in)
        return obj_in
