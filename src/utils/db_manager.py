from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository


class DBManager():
    def __init__(self,session_factory):
        self.session_factory = session_factory

    # команда сработает когда мы только входим в контекстный менеджер
    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepository(self.session)

        return self

    #команда когда мы выходим из контекстного менеджера. В арги передается 3 переменные для работы с ошибками
    async def __aexit__(self, *args):
        # Команда языка SQL. Если упала с ошибкой, то откатывает действия назад
        await self.session.rollback()

        await self.session.close()

    async def commit(self):
        await self.session.commit()