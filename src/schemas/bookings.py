from datetime import date
from pydantic import BaseModel, ConfigDict


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
    total_price: int | None
    created_at: date

    model_config = ConfigDict(from_attributes=True)