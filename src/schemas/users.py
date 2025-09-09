from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    age: int

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    nickname: str
    age: int

class User(BaseModel):
    id: int
    email: str
    nickname: str
    age: int

    model_config = ConfigDict(from_attributes=True)