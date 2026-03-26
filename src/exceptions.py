from datetime import date

from fastapi import HTTPException


class Nabroniroval(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ObjectNotFoundException(Nabroniroval):
    detail = "Object not found"

class HotelNotFoundException(Nabroniroval):
    detail = "Отель не найден"

class RoomNotFoundException(Nabroniroval):
    detail = "Номер не найден"

class AllRoomsAreBookedException(Nabroniroval):
    detail = "Не осталось свободных номеров"

class ObjectAlreadyExistsException(Nabroniroval):
    detail = "Object уже существует"

class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = "Object not found"
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code,detail=self.detail)

class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Отеля не существует"

class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Номер не существует"


def check_date_from_to(date_from: date, date_to: date):
    if date_to <= date_from:
        raise HTTPException(400, detail="Дата заезда позже даты выезда")