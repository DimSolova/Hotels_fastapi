from fastapi import APIRouter, HTTPException

from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingsAdd, BookingsAddRequest
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_bookings(db: DBDep):
    all_bookings = await db.bookings.get_all()
    return {"status": "ok", "data": all_bookings}


@router.get("/me")
async def get_user_bookings(user_id: UserIdDep, db: DBDep):
    user_bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "Ok", "data": user_bookings}


@router.post("")
async def add_bookings(
        user_id: UserIdDep,
        bookings_data: BookingsAddRequest,
        db: DBDep
):
    try:
        room: Room = await db.rooms.get_one(id=bookings_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=409, detail="Room not found")
    hotel_id: int = room.hotel_id
    room_price: int = room.price
    _bookings_data = BookingsAdd(user_id=user_id, price=room_price, **bookings_data.model_dump())
    try:
        data = await db.bookings.add_booking(
            _bookings_data,
            hotel_id,
        )
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": data}
