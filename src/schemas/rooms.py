from pydantic import BaseModel, Field

class RoomAdd(BaseModel):
    title: str
    hotel_id: int
    description: str
    price: int
    quantity: int

class Room(RoomAdd):
    id: int

class RoomPATCH(BaseModel):
    title: str | None = Field(None)
    hotel_id: int | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)