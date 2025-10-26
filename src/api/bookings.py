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
    room = await db.rooms.get_one_or_none(id=bookings_data.room_id)
    price: int = room.price
    _bookings_data = BookingsAdd(user_id=user_id, price=price, **bookings_data.model_dump())
    data = await db.bookings.add(_bookings_data)

    await db.commit()
    return {'status': 'ok', 'data': data}

@router.get('/bookings')
async def get_bookings(db:DBDep):
    all_bookings = await db.bookings.get_all()
    return {'status' : 'ok','data': all_bookings}

@router.get('/bookings/me')
async def get_user_bookings(user_id:UserIdDep,
                            db:DBDep):
    user_bookings = await db.bookings.get_filtered(user_id=user_id)
    return {'status': 'Ok', 'data': user_bookings}


