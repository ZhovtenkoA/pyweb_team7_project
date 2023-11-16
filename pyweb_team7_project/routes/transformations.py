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
from pyweb_team7_project.repository import transformations as repository_transformations
from pyweb_team7_project.services.auth import auth_service
from pyweb_team7_project.conf.config import settings
from pyweb_team7_project.schemas import UserDb, CreateImageModel, UpdateImageModel

router = APIRouter(prefix="/transformations", tags=["transformations"])

@router.patch('/transformations_grayscale/{image_id}')
async def transformations_grayscale(image_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):

    return await repository_transformations.transformations_grayscale(image_id = image_id, current_user = current_user, db = db)
    

@router.patch('/transformations_auto_color/{image_id}')
async def transformations_auto_color(image_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    
    return await repository_transformations.transformations_auto_color(image_id = image_id, current_user = current_user, db = db)


@router.patch('/transformations_sepia/{image_id}')
async def transformations_sepia(image_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    
    return await repository_transformations.transformations_sepia(image_id = image_id, current_user = current_user, db = db)


@router.patch('/transformations_blur/{image_id}')
async def transformations_blur(image_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    
    return await repository_transformations.transformations_blur(image_id = image_id, current_user = current_user, db = db)


@router.patch('/transformations_brown_outline/{image_id}')
async def transformations_brown_outline(image_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    
    return await repository_transformations.transformations_brown_outline(image_id = image_id, current_user = current_user, db = db)