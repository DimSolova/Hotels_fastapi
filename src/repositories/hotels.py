from sqlalchemy import select,func, insert
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower()))

        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower()))
        query = (query
                 .limit(limit)
                 .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self,data):
        query = await self.session.execute(
            insert(self.model).
            values(**data.model_dump()).
            returning(self.model.title, self.model.location))
        return query

