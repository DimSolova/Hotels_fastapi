from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import insert, select

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_price(self,room_id: int):
        stmt = select(self.model.price).where(self.model.id==room_id)
        res = await self.session.execute(stmt)
        price = res.scalar_one_or_none()
        return price

