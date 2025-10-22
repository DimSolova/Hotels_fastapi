from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix='/hotels',tags=['Номера'] )

@router.get('/{hotels_id}/rooms')
async def get_rooms(hotel_id:int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)

@router.get('/{hotels_id}/rooms/{room_id}')
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.post('/{hotels_id}/rooms',
             summary='Добавление номера',
             description='В request body передаем словарь со всеми параметрами ID '
                         'присвоиться автоматически')
#По REST мы обязаны передавать hotel_id в Query и что бы не передавать его
# 2 раза Query и Body мы создали специальную pydantic схему , где он принимает уже без hotel_id в теле Body(),
# это экономит время , так же удобно фронтэндеру
async def create_room(
        hotel_id: int,
        room_data: RoomAddRequest = Body(...)):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {'status': 'ok', 'data': room}

@router.put('/{hotels}/rooms/{room_id}',
            summary='Полное изменение отеля',
            description='передаем id отеля и json новых данных')
async def edit_room(hotel_id: int,
                    room_id: int,
                    room_data:RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data,
                                            id=room_id)
        await session.commit()
    return {'status': 'OK'}

@router.patch('/{hotels}/rooms/{room_id}',
              summary='частичное изменение отеля',
              description='передаем id и изменяем нужные нам '
                          'элементы в боди ')
async def partially_edit_room(hotel_id:int,
                              room_id: int,
                              room_data: RoomPatchRequest = Body(...)):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        #exclude_unset=True, метод в pydantic позволяет убрать
        #из словаря все значения в которых None
        await RoomsRepository(session).edit(_room_data,
                                            exclude_unset=True,
                                            id=room_id,
                                            hotel_id=hotel_id)
        await session.commit()
    return {'status': "ok"}

@router.delete('/{hotels}/rooms/{room_id}',
               summary='Удаляем номер',
               description='Нужно указать id комнаты которую хотим удалить')
async def delete(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}
