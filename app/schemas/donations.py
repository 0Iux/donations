from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt = Field(...,)


class DonationCreate(DonationBase):
    id: int
    create_date: datetime = Field(..., example="2010-10-10T00:00:00")

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    invested_amount: int = 0
    fully_invested: bool = Field(False)
    user_id: int

    class Config:
        orm_mode = True


class AllDonations(DonationCreate):
    pass
