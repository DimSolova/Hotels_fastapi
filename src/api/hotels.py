from datetime import date
from fastapi import Query, APIRouter, Body, HTTPException

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import check_date_from_to, ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получить все отели", description="Здесь мы выбираем отели")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(examples=["2024-07-01"]),
    date_to: date = Query(examples=["2024-11-10"]),
):
    hotels = await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )
    return {"status": "OK", "data": hotels}


@router.get(
    "/{hotel_id}", summary="Выбираем отель по ID", description="Вернет отель по выбранному ID"
)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post(
    "",
    summary="Добавление отеля",
    description="В request body передаем словарь со всеми параметрами ID присвоиться автоматически",
)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {
                    "title": "Hotel Sochi",
                    "location": "sochi u moria",
                },
            },
            "2": {
                "summary": "Minsk",
                "value": {
                    "title": "Minsk",
                    "location": "minsk",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "Ok", "data": hotel}


@router.delete(
    "/{hotel_id}",
    summary="Удаляем отель",
    description="Удаляем отель по ID",
)
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}


@router.put(
    "/{hotel_id}",
    summary="Изменение отеля",
    description="Полное изменение отеля, В Request body передаем словарь со всеми параметрами,"
    "он не может быть без какого либо элемента",
)
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).edit_hotel(hotel_data, hotel_id)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле",
)
async def partially_edit_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPATCH = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {"title": "Hotel Sochi", "location": "Russia Sochi"},
            },
            "2": {"summary": "Dubai", "value": {"title": "Dubai Hotel", "location": "Dubai"}},
        }
    ),
):
    await HotelService(db).partially_edit_hotel(hotel_data, hotel_id)
    return {"status": "OK"}
