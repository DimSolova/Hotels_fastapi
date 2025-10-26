from datetime import date
from pydantic import BaseModel



class BookingsAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class BookingsAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int

class Bookings(BookingsAdd):
    id: int
    user_id: int
    price: int