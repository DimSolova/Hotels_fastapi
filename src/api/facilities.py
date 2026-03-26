from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache


from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd
from src.services.facilities import FacilityService
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=20)
async def get_facilities(db: DBDep):
    print("go to db")
    return await db.facilities.get_all()


@router.post("")
async def add_facilities(db: DBDep, data: FacilitiesAdd = Body()):
    facility = await FacilityService(db).create_facility(data)
    return {"status": "ok", "falities": facility}
