from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.exceptions import check_date_from_to, ObjectNotFoundException, HotelNotFoundHTTPException, \
    RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
from src.schemas.facilities import RoomFacilitiesAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])



@router.get("/{hotels_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples=["2024-08-01"]),
    date_to: date = Query(examples=["2024-08-10"]),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)

@router.get("/{hotels_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление номера",
    description="В request body передаем словарь со всеми параметрами ID присвоиться автоматически",
)
# По REST мы обязаны передавать hotel_id в Query и что бы не передавать его
# 2 раза Query и Body мы создали специальную pydantic схему , где он принимает уже без hotel_id в теле Body(),
# это экономит время , так же удобно фронтэндеру
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body(...)):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "ok", "data": room}


@router.put(
    "/{hotels}/rooms/{room_id}",
    summary="Полное изменение отеля",
    description="передаем id отеля и json новых данных",
)
async def edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest):
    await RoomService(db).edit_room(hotel_id,room_id, room_data)
    return {"status": "OK"}


@router.patch(
    "/{hotels}/rooms/{room_id}",
    summary="частичное изменение отеля",
    description="передаем id и изменяем нужные нам элементы в боди ",
)
async def partially_edit_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest = Body(...)
):
    await RoomService(db).partially_edit_room(hotel_id,room_id,room_data)
    return {"status": "ok"}


@router.delete(
    "/{hotels}/rooms/{room_id}",
    summary="Удаляем номер",
    description="Нужно указать id комнаты которую хотим удалить",
)
async def delete(db: DBDep, hotel_id: int, room_id: int):
    await RoomService(db).delete(
        hotel_id,
        room_id
    )
    return {"status": "OK"}
