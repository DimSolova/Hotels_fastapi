from dns.e164 import query
from fastapi import Query,APIRouter, Body

from sqlalchemy import insert, select,func

from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from src.database import async_session_maker

router = APIRouter(prefix='/hotels', tags=['Отели'])

@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description='Location'),
        title: str | None = Query(None, description='Hotel name')
):
        per_page = pagination.per_page or 5
        async with async_session_maker() as session:
            query = select(HotelsOrm)
            if location:
                query = query.filter(func.lower(HotelsOrm.location).like(f'%{location.lower()}%'))

            if title:
                query = query.filter(func.lower(HotelsOrm.title).like(f'%{title.lower()}%'))
            query = (query
                     .limit(per_page)
                     .offset(per_page * (pagination.page - 1))
            )
            res = await session.execute(query)
            hotels = res.scalars().all()
            return hotels
        # if pagination.page and pagination.per_page:
        #     return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]


@router.post('')
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            "1": {'summary':'Sochi', 'value': {
                'title': 'Hotel Sochi',
                'location':'sochi u moria',
            }},
            "2": {'summary':'Minsk', 'value': {
                'title': 'Minsk',
                'location':'minsk',

        }}})
):
    async with async_session_maker() as session:
        add_hotel_statement = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_statement.compile(compile_kwargs={'literal_binds':True}))
        await session.execute(add_hotel_statement)
        await session.commit()
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