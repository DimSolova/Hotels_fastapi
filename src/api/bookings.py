from fastapi import APIRouter, HTTPException

from src.exceptions import AllRoomsAreBookedException, RoomNotFoundException, \
    RoomNotFoundHTTPException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingsAddRequest
from src.api.dependencies import UserIdDep, DBDep
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_bookings(db: DBDep):
    all_bookings = await BookingService(db).get_bookings()
    return {"status": "ok", "data": all_bookings}


@router.get("/me")
async def get_user_bookings(user_id: UserIdDep, db: DBDep):
    user_bookings = await BookingService(db).get_my_bookings(user_id)
    return {"status": "Ok", "data": user_bookings}


@router.post("")
async def add_bookings(
        user_id: UserIdDep,
        bookings_data: BookingsAddRequest,
        db: DBDep
):
    try:
        data = await BookingService(db).add_bookings(user_id, bookings_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": data}
