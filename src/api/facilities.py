import json
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from pydantic import BaseModel

from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get("")
@cache(expire=20)
async def get_facilities(db: DBDep):
    print("go to db")
    return await db.facilities.get_all()

@router.post("")
async def add_facilities(
        db: DBDep,
        data: FacilitiesAdd = Body()
                         ):
    facility = await db.facilities.add(data)
    await db.commit()

    return {"status": "ok","falities": facility}
