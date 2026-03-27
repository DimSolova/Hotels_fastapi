from datetime import datetime, timezone, timedelta

import bcrypt
import jwt

from src.config import setting
from src.exceptions import ObjectAlreadyExistsException, UserAlreadyExistsException, IncorrectTokenException, \
    EmailNotRegisteredException, IncorrectPasswordException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.base import BaseService


class AuthService(BaseService):
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, setting.JWT_SECRET_KEY, algorithm=setting.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGORITHM])
        except jwt.PyJWTError:
            raise IncorrectTokenException

    async def register_user(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def login_user(self, data):
        # проверка на существующий email
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException

        # проверка на верный пароль
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException

        # Создаем токен
        return self.create_access_token({"user_id": user.id})

    async def get_one_or_none(self, user_id: int):
        user = await self.db.users.get_one_or_none(id=user_id)
        return user

