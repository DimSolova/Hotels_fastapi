from fastapi import APIRouter, Body
from pydantic import BaseModel

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post("")
async def add_facilities(
        db: DBDep,
        data: FacilitiesAdd = Body()
                         ):
    facility = await db.facilities.add(data)
    await db.commit()

    return {"status": "ok","falities": facility}
