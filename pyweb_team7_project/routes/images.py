from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import and_
import cloudinary
from ..database.db import get_db
from ..database.models import User, Image
from ..repository import images as repository_images
from ..services.auth import auth_service
from fastapi_limiter.depends import RateLimiter
from ..schemas import CreateImageModel, UpdateImageModel, ImageResponse
from pyweb_team7_project.conf.config import settings
router = APIRouter(prefix='/images', tags=['images'])


@router.post("/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_image(
    description: str = Form(),
    tag_names: List[str] = Form([]),
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    return await repository_images.create_image_and_upload_to_cloudinary(db, file, description=description,
                                                                         user_id=current_user.id,
                                                                         tag_names=tag_names)


@router.get("/{image_id}", response_model=ImageResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_image(image_id: int, current_user: User = Depends(auth_service.get_current_user),
                    db: Session = Depends(get_db)):
    image = await repository_images.get_image_by_id(current_user, db, image_id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.put("/{image_id}", response_model=ImageResponse)
async def update_image(body: UpdateImageModel, image_id: int,
                       current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    image = await repository_images.update_image_description(current_user, db, image_id, body.description)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.delete("/{image_id}", response_model=ImageResponse)
async def delete_image(image_id: int, current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    image = await repository_images.delete_image(current_user, db, image_id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
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

    image.file_url = image_url
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

    image.file_url = image_url
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

    image.file_url = image_url
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

    image.file_url = image_url
    db.commit()
    db.refresh(image)
    return image
