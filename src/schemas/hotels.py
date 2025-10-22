from pydantic import BaseModel, Field, ConfigDict

class HotelAdd(BaseModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id: int

    # model_config = ConfigDict(from_attributes=True)

class HotelPATCH(BaseModel):
    # параметры могут быть как str так и None . = Field(None)
    # позволяет подробнее описать валидацию
    title: str | None = Field(None, description='Поле названия отеля')
    location: str | None = Field(None, description='Расположение отеля')