from sqlalchemy import Column, ForeignKey, Text, Integer

from app.models.base import BaseModel


class Donation(BaseModel):
    user_id = user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)
