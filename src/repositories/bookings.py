from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from src.database import engine
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from==date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self,data: BaseModel, hotel_id,):
        room_id = data.room_id
        rooms_ids_to_get = rooms_ids_for_booking(data.date_from, data.date_to, hotel_id)
        res = await self.session.execute(rooms_ids_to_get)
        rooms_ids = res.scalars().all()
        if room_id in rooms_ids:
            res = await self.add(data)
            return res
        else:
            raise HTTPException(500)