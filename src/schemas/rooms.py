from pydantic import BaseModel, Field, ConfigDict

from src.schemas.facilities import Facilities


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []

class RoomAdd(BaseModel):
    title: str
    hotel_id: int
    description: str | None = None
    price: int
    quantity: int

class Room(RoomAdd):
    id: int


    # model_config = ConfigDict(from_attributes=True)

class RoomWithRels(Room):
    facilities: list[Facilities]

class RoomPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] = []

class RoomPatch(BaseModel):
    title: str | None = Field(None)
    hotel_id: int | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)