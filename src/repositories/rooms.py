from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload, selectinload

from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomWithRels


class RoomsRepository(BaseRepository):
    model: RoomsOrm = RoomsOrm
    mapper = RoomDataMapper

    async def get_one_with_rels(self, **filter_by): #type: ignore
        query = (select(self.model)
                 .options(selectinload(self.model.facilities))
                 .filter_by(**filter_by)
                 )

        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException


        return RoomWithRels.model_validate(model, from_attributes=True)

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        # print(query.compile(bind=engine, compile_kwargs={'literal_binds': True}))

        query = (
            select(self.model) #type: ignore
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get)) #type: ignore
        )
        result = await self.session.execute(query)
        return [
            RoomWithRels.model_validate(model, from_attributes=True)
            for model in result.unique().scalars().all()
        ]

    # где используется эта функция
    # async def get_price(self,room_id: int):
    #     stmt = select(self.model.price).where(self.model.id==room_id)
    #     res = await self.session.execute(stmt)
    #     price = res.scalar_one_or_none()
    #     return price
