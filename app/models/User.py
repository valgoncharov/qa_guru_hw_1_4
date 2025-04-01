from pydantic import BaseModel, EmailStr, HttpUrl, ConfigDict, Field
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    job_title: str
    avatar: HttpUrl

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    data: User


class UserDelete(BaseModel):
    id: int
