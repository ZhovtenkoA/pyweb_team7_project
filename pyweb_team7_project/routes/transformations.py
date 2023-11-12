from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Path, File
from fastapi_limiter.depends import RateLimiter

from sqlalchemy.orm import Session
import cloudinary
from cloudinary.uploader import upload

from pyweb_team7_project.database.db import get_db
from pyweb_team7_project.database.models import User, Image
from pyweb_team7_project.repository import users as repository_users
from pyweb_team7_project.repository import images as repository_images
from pyweb_team7_project.services.auth import auth_service
from pyweb_team7_project.conf.config import settings
from pyweb_team7_project.schemas import UserDb, CreateImageModel, UpdateImageModel

router = APIRouter(prefix="/transformations", tags=["transformations"])

@router.patch('/transformations_upload_image')
async def upload_image(file: UploadFile = File()):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    # result = cloudinary.uploader.upload(file.file)
    result = upload(file.file)
    public_id = result['public_id']
    print("public_id "+public_id)
    return f'public_id{public_id}'

@router.patch('/transformations_grayscale/{public_id}')
async def transformations_grayscale(public_id: str):

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    
    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(public_id).image(effect="grayscale")
    return transformed_url

@router.patch('/transformations_auto_color/{public_id}')
async def transformations_auto_color(public_id: str):
    
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    
    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(public_id).image(effect="auto_color")
    return transformed_url

@router.patch('/transformations_sepia/{public_id}')
async def transformations_sepia(public_id: str):
    
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    
    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(public_id).image(effect="sepia")
    return transformed_url

@router.patch('/transformations_blur/{public_id}')
async def transformations_blur(public_id: str):
    
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    
    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(public_id).image(effect="blur:300")
    return transformed_url

@router.patch('/transformations_brown_outline/{public_id}')
async def transformations_brown_outline(public_id: str):
    
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    
    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(public_id).image(effect="co_brown,e_outline")
    return transformed_url