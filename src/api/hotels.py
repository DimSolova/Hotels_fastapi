from fastapi import Query,APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd

router = APIRouter(prefix='/hotels', tags=['Отели'])

@router.get('',
            summary='Получить все отели',
            description='Здесь мы выбираем отели')
async def get_hotels(
        pagination: PaginationDep,
        db:DBDep,
        location: str | None = Query(None, description='Локация'),
        title: str | None = Query(None, description='Название отеля')
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get('/{hotel_id}',
            summary='Выбираем отель по ID',
            description='Вернет отель по выбранному ID')
async def get_hotel_id(hotel_id:int, db:DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post('',
             summary='Добавление отеля',
             description='В request body передаем словарь со всеми параметрами ID '
                         'присвоиться автоматически')
async def create_hotel(
        db:DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {'summary':'Sochi', 'value': {
                'title': 'Hotel Sochi',
                'location':'sochi u moria',
            }},
            "2": {'summary':'Minsk', 'value': {
                'title': 'Minsk',
                'location':'minsk',

        }}})
):
    data = await db.hotels.add(hotel_data)
    await db.commit()
    return {'status': 'Ok', "data": data}


@router.delete('/{hotel_id}',
               summary='Удаляем отель',
               description='Удаляем отель по ID',)
async def delete_hotel(db:DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status': 'OK'}

@router.put("/{hotel_id}",
            summary='Изменение отеля',
            description='Полное изменение отеля, В Request body передаем словарь со всеми параметрами,'
                        'он не может быть без какого либо элемента')
async def edit_hotel(db:DBDep,
                     hotel_id: int,
                     hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data,
                         id=hotel_id)
    await db.commit()
    return {'status': 'OK'}

@router.patch("/{hotel_id}",
           summary='Частичное обновление данных об отеле',
           description="Тут мы частично обновляем данные об отеле")
async def partially_edit_hotel(
        db:DBDep,
        hotel_id : int,
        hotel_data: HotelPATCH = Body(openapi_examples={
            '1': {'summary' : 'Sochi', 'value': {
                'title': 'Hotel Sochi',
                'location': 'Russia Sochi'

            }

                                                              },
            '2': {'summary': 'Dubai', 'value': {
                'title': 'Dubai Hotel',
                'location': 'Dubai'
            }}})
):
    #exclude_unset=True удаляет поля, где = None
    await db.hotels.edit(hotel_data,
                         exclude_unset=True,
                         id=hotel_id)
    await db.commit()
    return {'status': 'OK'}