from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, EmailStr
from pyweb_team7_project.database.models import Role


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    role: Role 
    class Config:
        orm_mode = True


class ResponseUser(BaseModel):
    user: UserDb
    detatil: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class EmailSchema(BaseModel):
    email: EmailStr


class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int
    name: str = Field(max_length=25)

    class Config:
        from_attributes = True


class CommentRequestModel(BaseModel):
    image_id: int
    content: str = Field(max_length=250)


class CommentUpdateModel(BaseModel):
    content: str = Field(max_length=250)


class CommentResponseModel(BaseModel):
    id: int
    user_id: int
    image_id: int
    content: str = Field(max_length=250)
    created_at: datetime
    edited_at: datetime


class CreateImageModel(BaseModel):
    description: str
    tag_names: List[str] = []


class UpdateImageModel(BaseModel):
    new_description: str


class ImageResponse(BaseModel):
    id: int
    file_url: str
    description: str
    user_id: int

    # tags: List[str]

    class Config:
        orm_mode = True


class QRCodeRequestTest(BaseModel):
    qr_data: str = Field("https://github.com/ZhovtenkoA/pyweb_team7_project", max_length=250)


class QRCodeResponse(BaseModel):
    qrcode_cloud_url: str = Field(max_length=250)
