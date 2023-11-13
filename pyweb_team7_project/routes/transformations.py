from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Path, File
from fastapi_limiter.depends import RateLimiter

from sqlalchemy import and_
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
async def upload_image(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    # result = cloudinary.uploader.upload(file.file)
    result = upload(file.file)
    # Отримуємо public ID завантаженого зображення
    public_id = result['public_id']
    # Отримайте URL обробленого зображення
    fileurl = result["secure_url"]

    user = db.query(User).filter_by(id=current_user.id).first()
    if not user:
        raise Exception("User not found")

    image = Image(fileurl=fileurl, public_id=public_id, user_id=current_user.id)
    db.add(image)
    db.commit()
    db.refresh(image)
    
    # image = repository_images.create_image(db=db, fileurl=fileurl, public_id=public_id, user_id=current_user.id)
    return image

@router.patch('/transformations_grayscale/{image_id}')
async def transformations_grayscale(image_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):

    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    
    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(image.public_id).image(effect="grayscale")
    # Отримання тільки посилання з рядка HTML
    url_start = transformed_url.find("src=\"") + 5
    url_end = transformed_url.find("\"", url_start)
    image_url = transformed_url[url_start:url_end]

    image.fileurl = image_url
    db.commit()
    db.refresh(image)
    return image

@router.patch('/transformations_auto_color/{image_id}')
async def transformations_auto_color(image_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    
    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(image.public_id).image(effect="auto_color")
    # Отримання тільки посилання з рядка HTML
    url_start = transformed_url.find("src=\"") + 5
    url_end = transformed_url.find("\"", url_start)
    image_url = transformed_url[url_start:url_end]

    image.fileurl = image_url
    db.commit()
    db.refresh(image)
    return image

@router.patch('/transformations_sepia/{image_id}')
async def transformations_sepia(image_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    
    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(image.public_id).image(effect="sepia")
    # Отримання тільки посилання з рядка HTML
    url_start = transformed_url.find("src=\"") + 5
    url_end = transformed_url.find("\"", url_start)
    image_url = transformed_url[url_start:url_end]

    image.fileurl = image_url
    db.commit()
    db.refresh(image)
    return image

@router.patch('/transformations_blur/{image_id}')
async def transformations_blur(image_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    
    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(image.public_id).image(effect="blur:300")
    # Отримання тільки посилання з рядка HTML
    url_start = transformed_url.find("src=\"") + 5
    url_end = transformed_url.find("\"", url_start)
    image_url = transformed_url[url_start:url_end]

    image.fileurl = image_url
    db.commit()
    db.refresh(image)
    return image

@router.patch('/transformations_brown_outline/{image_id}')
async def transformations_brown_outline(image_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    
    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(image.public_id).image(effect="co_brown,e_outline")
    # Отримання тільки посилання з рядка HTML
    url_start = transformed_url.find("src=\"") + 5
    url_end = transformed_url.find("\"", url_start)
    image_url = transformed_url[url_start:url_end]

    image.fileurl = image_url
    db.commit()
    db.refresh(image)
    return image