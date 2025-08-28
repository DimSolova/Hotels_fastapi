from fastapi import Query,APIRouter, Body


from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH
from src.database import async_session_maker

router = APIRouter(prefix='/hotels', tags=['Отели'])

@router.get('/{hotel_id}')
async def get_hotel_id(hotel_id:int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description='Location'),
        title: str | None = Query(None, description='Hotel name')
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


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
        data = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {'status': 'Ok', "data": data}


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}

@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int,
                     hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data,
                                                   id=hotel_id)
        await session.commit()
    return {'status': 'OK'}

@router.patch("/{hotel_id}",
           summary='Частичное обновление данных об отеле',
           description="Тут мы частично обновляем данные об отеле")
async def partially_edit_hotel(
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
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data,
                                             exclude_unset=True,
                                             id=hotel_id)
        await session.commit()
    return {'status': 'OK'}