from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..database.models import User, Image
from ..repository import images as repository_images
from ..services.auth import auth_service
from fastapi_limiter.depends import RateLimiter
from ..schemas import CreateImageModel, UpdateImageModel, ImageResponse
router = APIRouter(prefix='/images', tags=['images'])


@router.post("/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_image(body: CreateImageModel, current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    return await repository_images.create_image(db, filename=body.filename, description=body.description,
                                                user_id=current_user.id, tag_names=body.tag_names)


@router.get("/{image_id}", response_model=ImageResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_image(image_id: int = Path(...), current_user: User = Depends(auth_service.get_current_user),
                    db: Session = Depends(get_db)):
    image = await repository_images.get_image_by_id(current_user, db, image_id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.put("/{image_id}", response_model=ImageResponse)
async def update_image(body: UpdateImageModel, image_id: int = Path(...),
                       current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    image = await repository_images.update_image_description(current_user, db, image_id, body.description)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.delete("/{image_id}", response_model=ImageResponse)
async def delete_image(image_id: int = Path(...), current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    image = await repository_images.delete_image(current_user, db, image_id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image

