from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from src.schemas.hotels import Hotel


class BaseRepository():
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self,*args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        model =  result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_data_statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        model = await self.session.execute(add_data_statement)
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self, data: BaseModel,exclude_unset:bool = False, **filter_by) -> None:

        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(update_stmt)

    async def delete(self, **filter) -> None:
        delete_stmt = delete(self.model).filter_by(**filter)
        await self.session.execute(delete_stmt)
