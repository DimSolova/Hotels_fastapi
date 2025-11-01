from datetime import date

from sqlalchemy import select, func

from src.database import engine
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import Bookings
from src.schemas.rooms import Room



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        # print(query.compile(bind=engine, compile_kwargs={'literal_binds': True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
    #где используется эта функция
    # async def get_price(self,room_id: int):
    #     stmt = select(self.model.price).where(self.model.id==room_id)
    #     res = await self.session.execute(stmt)
    #     price = res.scalar_one_or_none()
    #     return price

