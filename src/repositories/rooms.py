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
        print(hotel_id,date_from,date_to)
        """
        with rooms_count as (
            select room_id,count(*) as rooms_booked from bookings
            where date_from <= '2024-11-07' and date_to >= '2024-07-01'
            group by room_id
        ),
        rooms_left_table as (
        select rooms.id as room_id , quantity - coalesce(rooms_booked, 0) as rooms_left
        from rooms
        left join rooms_count on rooms.id = rooms_count.room_id
        )
        select * from rooms_left_table
        where rooms_left > 0
        """

        '''select room_id,count(*) as rooms_booked from bookings
            where date_from <= '2024-11-07' and date_to >= '2024-07-01'
            group by room_id'''

        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= '2024-11-07',
                BookingsOrm.date_to >= '2024-07-01'
            )
            .group_by(BookingsOrm.room_id)
            .cte(name='rooms_count')
        )
        """select rooms.id as room_id , quantity - coalesce(rooms_booked, 0) as rooms_left
        from rooms
        left join rooms_count on rooms.id = rooms_count.room_id"""
        rooms_left_table = (
            select(RoomsOrm.id.label("room_id"),
                   (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        '''
        select * from rooms_left_table
        where rooms_left > 0
        '''

        query = (
            select(rooms_left_table)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0)
        )
        print(query.compile(bind=engine, compile_kwargs={'literal_binds': True}))
    #где используется эта функция
    # async def get_price(self,room_id: int):
    #     stmt = select(self.model.price).where(self.model.id==room_id)
    #     res = await self.session.execute(stmt)
    #     price = res.scalar_one_or_none()
    #     return price

