from fastapi import APIRouter

from src.schemas.bookings import BookingsAdd, BookingsAddRequest
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix='/bookings', tags=['Бронирование'])

@router.post('')
async def add_bookings(
        user_id: UserIdDep,
        bookings_data: BookingsAddRequest,
        db: DBDep
):
    price = await db.rooms.get_price(bookings_data.model_dump()['room_id'])
    _bookings_data = BookingsAdd(user_id=user_id, price=price, **bookings_data.model_dump())
    data = await db.bookings.add(_bookings_data)

    await db.commit()
    return {'status': 'ok', 'data': data}


