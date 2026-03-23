# src/api/auth.py
from fastapi import APIRouter, HTTPException, Response, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await db.users.add(new_user_data)
        await db.commit()
    except:
        raise HTTPException(status_code=400)


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
    # проверка на существующий email
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")

    # проверка на верный пароль
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль не верный")

    # Создаем токен
    access_token = AuthService().create_access_token({"user_id": user.id})
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
    user = await db.users.get_one_or_none(id=user_id)
    return user
