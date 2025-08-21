from fastapi import Query,APIRouter, Body

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])




hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'},
]


@router.get('')
def get_hotels(
        id: int | None = Query(None, description='Id'),
        title: str | None = Query(None, description='Hotel name')
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post('')
def create_hotel(
        hotel_data: Hotel
):
    async with se
    return {'status': 'Ok'}


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

@router.put("/{hotel_id}")
def edit_hotel(hotel_id:int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    hotel['title'] = hotel_data.title
    hotel['name'] = hotel_data.name
    return {'status': 'OK'}

@router.patch("/{hotel_id}",
           summary='Частичное обновление данных об отеле',
           description="Тут мы частично обновляем данные об отеле")
def partially_edit_hotel(
        hotel_id : int,
        hotel_data: HotelPATCH = Body(openapi_examples={
            '1': {'summary' : 'Sochi', 'value': {
                'title': 'Hotel Sochi',
                'name': 'hotel about ocean'

            }

                                                              },
            '2': {'summary': 'Dubai', 'value': {
                'title': 'Dubai',
                'name': 'dubai eptel'
            }}})
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    if hotel_data.title:
        hotel['title'] = hotel_data.title
    if hotel_data.name:
        hotel['name'] = hotel_data.name
    return {'status': 'OK'}