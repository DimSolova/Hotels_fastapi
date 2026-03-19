from datetime import date
from pydantic import BaseModel, ConfigDict, Field


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

class BookingsPATCH(BaseModel):
    user_id: int | None = Field(None)
    room_id: int | None = Field(None)
    date_from: date | None = Field(None)
    date_to: date | None = Field(None)
    price: int | None = Field(None)

class Bookings(BookingsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)