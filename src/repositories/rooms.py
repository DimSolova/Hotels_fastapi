from datetime import date

from sqlalchemy import select, func

from src.database import engine
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
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

        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from
            )
            .group_by(BookingsOrm.room_id)
            .cte(name='rooms_count')
        )

        rooms_left_table = (
            select(RoomsOrm.id.label("room_id"),
                   (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        rooms_ids_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name='rooms_ids_for_hotel')
        )

        rooms_ids_to_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel)
            )
        )
        # print(query.compile(bind=engine, compile_kwargs={'literal_binds': True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
    #где используется эта функция
    # async def get_price(self,room_id: int):
    #     stmt = select(self.model.price).where(self.model.id==room_id)
    #     res = await self.session.execute(stmt)
    #     price = res.scalar_one_or_none()
    #     return price

