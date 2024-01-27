from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt
    pass


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = Field(False)
    create_date: datetime = Field(..., example="2010-10-10T00:00:00")
    close_date: Optional[datetime] = Field(None, example="2010-10-10T00:00:00")

    class Config:
        orm_mode = True
