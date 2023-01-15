from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    login: str
    password: str

class CreateUser(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True