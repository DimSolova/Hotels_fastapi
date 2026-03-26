from datetime import date

from src.exceptions import check_date_from_to, ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPATCH, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
            self,
            pagination,
            location: str | None,
            title: str | None,
            date_from: date,
            date_to: date,
    ):
        check_date_from_to(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )

    async def get_hotel(self, hotel_id):
        await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def delete_hotel(self,hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def edit_hotel(self, data: HotelAdd, hotel_id: int):
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def partially_edit_hotel(self, data: HotelPATCH, hotel_id: int):
        # exclude_unset=True удаляет поля, где = None
        await self.db.hotels.edit(data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException