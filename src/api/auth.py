# src/api/auth.py
from fastapi import APIRouter, Response, Body

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import UserAlreadyExistsException, UserEmailAlreadyExistsException, \
    EmailNotRegisteredException, IncorrectPasswordException, EmailNotRegisteredHTTPException, \
    IncorrectPasswordHTTPException
from src.schemas.users import UserRequestAdd, UserLogin
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
        db: DBDep,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsException

@router.post("/login")
async def login_user(
    response: Response,
    db: DBDep,
    data: UserLogin = Body(
        openapi_examples={
            "1": {
                "summary": "Dima_Solova",
                "value": {"email": "dimsolova@gmail.com", "password": "string"},
            },
            "2": {"summary": "Sveta", "value": {"email": "sveta@gmail.com", "password": "string"}},
            "3": {"summary": "Ira", "value": {"email": "ira@gmail.com", "password": "string"}},
        }
    ),
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "токен удален"}


@router.get("/me", description="проверяет есть ли в куках jwt токен и возвращает пользователя")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    return await AuthService(db).get_one_or_none(user_id)
