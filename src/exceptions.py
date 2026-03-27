from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ObjectNotFoundException(NabronirovalException):
    detail = "Object not found"

class HotelNotFoundException(NabronirovalException):
    detail = "Отель не найден"

class RoomNotFoundException(NabronirovalException):
    detail = "Номер не найден"

class EmailNotRegisteredException(NabronirovalException):
    detail = "Пользователь с таким email не зарегистрирован"

class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"

class IncorrectTokenException(NabronirovalException):
    detail = "Неверный токен"

class IncorrectPasswordException(NabronirovalException):
    detail = "Пароль не верный"

class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Object уже существует"

class UserAlreadyExistsException(NabronirovalException):
    detail = "Пользователь уже существует"


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

class UserEmailAlreadyExistsException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"

class EmailNotRegisteredHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой не зарегистрирован"

class IncorrectTokenHTTPException(NabronirovalHTTPException):
    #TODO  переделать статус код -> возвращаем 500 (так нельзя)
    status_code = 401
    detail = "Некорректный токен"

class IncorrectPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пароль не верный"



def check_date_from_to(date_from: date, date_to: date):
    if date_to <= date_from:
        raise HTTPException(400, detail="Дата заезда позже даты выезда")

