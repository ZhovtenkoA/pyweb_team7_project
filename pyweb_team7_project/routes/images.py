from typing import List

import cloudinary
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import and_
from sqlalchemy.orm import Session

from pyweb_team7_project.conf.config import settings
from ..database.db import get_db
from ..database.models import User, Image, Role
from ..repository import images as repository_images
from ..schemas import UpdateImageModel, ImageResponse
from ..services.auth import auth_service

from pyweb_team7_project.services.roles import RoleAccess
from pyweb_team7_project.services.roles import free_access, admin_user

access_to_images = RoleAccess([Role.admin])

router = APIRouter(prefix="/images", tags=["Images"])


@router.post(
    "/",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=2, seconds=5)), Depends(free_access)],
)
async def create_image(
    description: str = Form(),
    tags: str = Form(default=""),
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new image.

    :param description: The description of the image.
    :type description: str
    :param tags: Tags associated with the image separated by commas.
    :type tags: str
    :param file: The image file to be uploaded.
    :type file: UploadFile
    :param current_user: The current authenticated user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :raises HTTPException: If the number of tags exceeds 5 or the length of a tag name exceeds 25 characters.
    :return: The created image.
    :rtype: ImageResponse
    """
    tag_list = []
    if tags:
        tag_list = tags.split(", ")
        if len(tag_list) > 5:
            raise HTTPException(
                status_code=400, detail="You can't add more than 5 tags to a photo."
            )
        for tag in tag_list:
            if len(tag) > 25:
                raise HTTPException(
                    status_code=400,
                    detail="Tag name should be no more than 25 characters long.",
                )
    image = await repository_images.create_image_and_upload_to_cloudinary(
        db, file, description=description, user_id=current_user.id, tag_names=tag_list
    )

    return image


@router.get(
    "/{image_id}",
    response_model=ImageResponse,
    dependencies=[Depends(RateLimiter(times=2, seconds=5)), Depends(free_access)],
)
async def get_image(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get an image by its ID.

    :param image_id: The ID of the image.
    :type image_id: int
    :param current_user: The current authenticated user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :raises HTTPException: If the image is not found.
    :return: The retrieved image.
    :rtype: ImageResponse
    """
    image = await repository_images.get_image_by_id(current_user, db, image_id)
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    return image


@router.get(
    "/",
    response_model=List[ImageResponse],
    dependencies=[Depends(RateLimiter(times=2, seconds=5)), Depends(free_access)],
)
async def get_all_images(db: Session = Depends(get_db)):
    """
    Get all images.

    :param db: The database session.
    :type db: Session
    :return: A list of all images.
    :rtype: List[ImageResponse]
    """
    images = await repository_images.get_all_images(db)
    return images


@router.put(
    "/{image_id}", response_model=ImageResponse, dependencies=[Depends(admin_user)]
)
async def update_image(
    body: UpdateImageModel,
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the description of an image.

    :param image_id: The ID of the image.
    :type image_id: int
    :param body: The updated image model.
    :type body: UpdateImageModel
    :param current_user: The current authenticated user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :raises HTTPException: If the image is not found or the user does not have permission to update the image.
    :return: The updated image.
    :rtype: ImageResponse
    """
    image = await repository_images.get_image_by_id(
        user=current_user, image_id=int(image_id), db=db
    )
    if image:
        if current_user.id != image.user_id and current_user.role != Role.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
            )
        image = await repository_images.update_image_description(
            current_user, db, image_id, body.new_description
        )
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    return image


@router.delete("/{image_id}", response_model=None, dependencies=[Depends(admin_user)])
async def delete_image(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete an image by its ID.

    :param image_id: The ID of the image.
    :type image_id: int
    :param current_user: The current authenticated user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :raises HTTPException: If the image is not found or the user does not have permission to delete the image.
    """
    image = await repository_images.get_image_by_id(
        user=current_user, image_id=int(image_id), db=db
    )
    if image:
        if current_user.id != image.user_id and current_user.role != Role.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
            )
        image = await repository_images.delete_image(current_user, db, image_id)
        return image
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )


@router.patch("/transformations_grayscale/{image_id}")
async def transformations_grayscale(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Apply grayscale transformation to an image.

    :param image_id: The ID of the image.
    :type image_id: int
    :param current_user: The current user. Dependency on auth_service.get_current_user.
    :type current_user: User, optional
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The transformed image.
    :rtype: Image
    """
    image = (
        db.query(Image)
        .filter(and_(Image.id == image_id, Image.user_id == current_user.id))
        .first()
    )

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(image.public_id).image(
        effect="grayscale"
    )
    # Отримання тільки посилання з рядка HTML
    url_start = transformed_url.find('src="') + 5
    url_end = transformed_url.find('"', url_start)
    image_url = transformed_url[url_start:url_end]

    image.file_url = image_url
    db.commit()
    db.refresh(image)
    return image


@router.patch("/transformations_auto_color/{image_id}")
async def transformations_auto_color(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Apply auto color transformation to an image.

    :param image_id: The ID of the image.
    :type image_id: int
    :param current_user: The current user. Dependency on auth_service.get_current_user.
    :type current_user: User, optional
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The transformed image.
    :rtype: Image
    """
    image = (
        db.query(Image)
        .filter(and_(Image.id == image_id, Image.user_id == current_user.id))
        .first()
    )

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(image.public_id).image(
        effect="auto_color"
    )
    # Отримання тільки посилання з рядка HTML
    url_start = transformed_url.find('src="') + 5
    url_end = transformed_url.find('"', url_start)
    image_url = transformed_url[url_start:url_end]

    image.file_url = image_url
    db.commit()
    db.refresh(image)
    return image


@router.patch("/transformations_sepia/{image_id}")
async def transformations_sepia(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Apply sepia transformation to an image.

    :param image_id: The ID of the image.
    :type image_id: int
    :param current_user: The current user. Dependency on auth_service.get_current_user.
    :type current_user: User, optional
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The transformed image.
    :rtype: Image
    """
    image = (
        db.query(Image)
        .filter(and_(Image.id == image_id, Image.user_id == current_user.id))
        .first()
    )

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(image.public_id).image(effect="sepia")
    # Отримання тільки посилання з рядка HTML
    url_start = transformed_url.find('src="') + 5
    url_end = transformed_url.find('"', url_start)
    image_url = transformed_url[url_start:url_end]

    image.file_url = image_url
    db.commit()
    db.refresh(image)
    return image


@router.patch("/transformations_blur/{image_id}")
async def transformations_blur(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Apply blur effect to an image.

    :param image_id: The ID of the image.
    :type image_id: int
    :param current_user: The current user. Dependency on auth_service.get_current_user.
    :type current_user: User, optional
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The transformed image.
    :rtype: Image
    """
    image = (
        db.query(Image)
        .filter(and_(Image.id == image_id, Image.user_id == current_user.id))
        .first()
    )

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(image.public_id).image(
        effect="blur:300"
    )
    # Отримання тільки посилання з рядка HTML
    url_start = transformed_url.find('src="') + 5
    url_end = transformed_url.find('"', url_start)
    image_url = transformed_url[url_start:url_end]

    image.fileurl = image_url
    db.commit()
    db.refresh(image)
    return image


@router.patch("/transformations_brown_outline/{image_id}")
async def transformations_brown_outline(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Apply brown outline effect to an image.

    :param image_id: The ID of the image.
    :type image_id: int
    :param current_user: The current user. Dependency on auth_service.get_current_user.
    :type current_user: User, optional
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The transformed image.
    :rtype: Image
    """
    image = (
        db.query(Image)
        .filter(and_(Image.id == image_id, Image.user_id == current_user.id))
        .first()
    )

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    # Застосовуємо трансформації та отримуємо новий URL
    transformed_url = cloudinary.CloudinaryImage(image.public_id).image(
        effect="co_brown,e_outline"
    )
    # Отримання тільки посилання з рядка HTML
    url_start = transformed_url.find('src="') + 5
    url_end = transformed_url.find('"', url_start)
    image_url = transformed_url[url_start:url_end]

    image.file_url = image_url
    db.commit()
    db.refresh(image)
    return image


@router.post("/qr_code/")
async def get_qr_code(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get the QR code for an image.

    :param image_id: The ID of the image.
    :type image_id: int
    :param current_user: The current user. Dependency on auth_service.get_current_user.
    :type current_user: User, optional
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The QR code URL.
    :rtype: str
    """
    qr_url = await repository_images.get_QR(image_id, db)
    if qr_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found, can't get QR",
        )
    return qr_url
