from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomPATCH
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix='/rooms',tags=['Номера'] )

@router.get('')
async def get_rooms():
    async with async_session_maker() as session:
        data = await RoomsRepository(session).get_all()
    return {'status' : 'ok','data': data}

@router.post('',
             summary='Добавление номера',
             description='В request body передаем словарь со всеми параметрами ID '
                         'присвоиться автоматически')
async def create_room(
        room_data: RoomAdd = Body(...)):
    async with async_session_maker() as session:
        data = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {'status': 'ok', 'data': data}

@router.delete('/{room_id}',
               summary='Удаляем номер',
               description='Нужно указать id комнаты которую хотим удалить')
async def delete(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {'status': 'OK'}

@router.put('/{room_id}',
            summary='Полное изменение отеля',
            description='передаем id отеля и json новых данных')
async def edit_room(room_id: int,
                    room_data:RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data,
                                            id=room_id)
        await session.commit()
    return {'status': 'OK'}

@router.patch('/{room_id}',
              summary='частичное изменение отеля',
              description='передаем id и изменяем нужные нам '
                          'элементы в боди ')
async def partially_edit_room(room_id: int,
                              room_data: RoomPATCH = Body(...)):
    async with async_session_maker() as session:
        #exclude_unset=True, метод в pydantic позволяет убрать
        #из словаря все значения в которых None
        await RoomsRepository(session).edit(room_data,
                                            exclude_unset=True,
                                            id=room_id)
        await session.commit()
    return {'status': "ok"}
