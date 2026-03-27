from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundException
from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.schemas.rooms import Room
from src.services.base import BaseService


class BookingService(BaseService):

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_bookings(self, user_id: int, bookings_data: BookingsAddRequest):
        try:
            room: Room = await self.db.rooms.get_one(id=bookings_data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        hotel_id: int = room.hotel_id
        room_price: int = room.price
        _bookings_data = BookingsAdd(user_id=user_id, price=room_price, **bookings_data.model_dump())
        booking = await self.db.bookings.add_booking(
            _bookings_data,
            hotel_id,
        )
        await self.db.commit()
        return booking