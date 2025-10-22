from dns.e164 import query
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import insert, select

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

# TODO в функции выполняется проверка , а остальная часть кода такая же как и в base.py
    async def add(self,data : BaseModel):
        #проверка на корректный hotel_id
        hotel_check = await self.session.execute(select(HotelsOrm).
                                                 where(HotelsOrm.id == data.hotel_id))
        if not hotel_check.scalars().first():
            raise HTTPException(status_code=400, detail='такого hotel_id не существует')

        # переписываем метод из base
        add_data_statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_statement)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def get_all(self):
        query = select(RoomsOrm)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]