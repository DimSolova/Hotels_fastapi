from pydantic import BaseModel
from sqlalchemy import insert

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import Bookings


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Bookings

    async def add(self, data: BaseModel):
        _data = data.model_dump()
        add_bookings_statement = insert(self.model).values(data.model_dump()).returning(self.model)
        res = await self.session.execute(add_bookings_statement)
        model = res.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)
