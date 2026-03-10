import json
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from pydantic import BaseModel

from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    # print("go to db")
    # return await db.facilities.get_all()

    facilities_from_cache = await redis_manager.get("facilities")
    print(f"{facilities_from_cache=}")
    if not facilities_from_cache:
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json)
        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts


@router.post("")
async def add_facilities(
        db: DBDep,
        data: FacilitiesAdd = Body()
                         ):
    facility = await db.facilities.add(data)
    await db.commit()

    return {"status": "ok","falities": facility}
