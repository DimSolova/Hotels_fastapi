from fastapi import APIRouter, Path
from src.api.dependencies import PracticeParams, PracticeDep, PracticeUser
from typing import Annotated

router = APIRouter(prefix='/practice', tags=['Практика'])

@router.get('/square')
async def get(number: PracticeDep

):
    """Возвращает квадрат числа"""
    print(number.model_dump()['number'], type(number.model_dump()))
    return {'number': number, "square": number ** 2}

@router.get("/users/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(..., ge=1, description="ID пользователя >= 1")]
):
    return {"message": f"Пользователь с id={user_id}"}

@router.post('/users')
async def create_users(user: PracticeUser):
    print(user.model_dump())
    return {user.model_dump()['name'], user.model_dump()['age']}