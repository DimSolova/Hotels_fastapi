from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import DBDep, UserIdDep
from passlib.context import CryptContext
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

@router.post("/register")
async def register_user(
        db:DBDep,
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)

    #В переменной алембик схема
    new_user_data = UserAdd(email=data.email,
                            hashed_password=hashed_password,
                            nickname=data.nickname,
                            age=data.age)
    user = await db.users.get_user_with_hashed_password(email=data.email)

        # проверка на существующий email
    if user:
        raise HTTPException(status_code=401, detail='Пользователь с таким email зарегистрирован')

    await db.users.add(new_user_data)
    await db.commit()
    return {'status': 'OK'}

@router.post('/login')
async def login_user(
        data: UserRequestAdd,
        response: Response,
        db: DBDep
):
    user = await db.users.get_user_with_hashed_password(email=data.email)

    #проверка на существующий email
    if not user:
        raise HTTPException(status_code=401, detail='Пользователь с таким email не зарегистрирован')

    #проверка на верный пароль
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Пароль не верный')

    # Создаем токен
    access_token = AuthService().create_access_token({'user_id': user.id,
                                                      'age': user.age})
    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}

@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key='access_token')
    return {'status': 'токен удален'}

@router.get('/me',
            description='проверяет есть ли в куках jwt токен и возвращает пользователя')
async def get_me(
        user_id: UserIdDep,
        db:DBDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user
