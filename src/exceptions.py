class Nabroniroval(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ObjectNotFoundException(Nabroniroval):
    detail = "Object not found"