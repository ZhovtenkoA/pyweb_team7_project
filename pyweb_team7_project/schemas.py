from typing import List
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    
    class Config:
        form_attributes = True


class ResponseUser(BaseModel):
    user: UserDb
    detatil: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class EmailSchema(BaseModel):
    email: EmailStr


class CreateImageModel(BaseModel):
    filename: str
    description: str
    tag_names: List[str] = []


class UpdateImageModel(BaseModel):
    new_description: str


class ImageResponse(BaseModel):
    id: int
    filename: str
    description: str
    user_id: int
    tags: List[str]  # Assuming Tag has a 'name' attribute

    class Config:
        orm_mode = True