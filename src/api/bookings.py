from fastapi import APIRouter


router = APIRouter(prefix='/bookings', tags=['Бронирование'])

@router.post('')
async def add_bookings():
    return {'status': 'ok'}


