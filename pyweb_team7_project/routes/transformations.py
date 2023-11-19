from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Path, File
from fastapi_limiter.depends import RateLimiter


from sqlalchemy.orm import Session


from pyweb_team7_project.database.db import get_db
from pyweb_team7_project.database.models import User

from pyweb_team7_project.repository import transformations as repository_transformations
from pyweb_team7_project.services.auth import auth_service


router = APIRouter(prefix="/transformations", tags=["transformations"])


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
    :return: The updated ImageResponse object representing the transformed image.
    :rtype: ImageResponse
    """

    return await repository_transformations.transformations_grayscale(
        image_id=image_id, current_user=current_user, db=db
    )


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
    :return: The updated ImageResponse object representing the transformed image.
    :rtype: ImageResponse
    """

    return await repository_transformations.transformations_auto_color(
        image_id=image_id, current_user=current_user, db=db
    )


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
    :return: The updated ImageResponse object representing the transformed image.
    :rtype: ImageResponse
    """

    return await repository_transformations.transformations_sepia(
        image_id=image_id, current_user=current_user, db=db
    )


@router.patch("/transformations_blur/{image_id}")
async def transformations_blur(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Apply blur transformation to an image.

    :param image_id: The ID of the image.
    :type image_id: int
    :param current_user: The current user. Dependency on auth_service.get_current_user.
    :type current_user: User, optional
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The updated ImageResponse object representing the transformed image.
    :rtype: ImageResponse
    """

    return await repository_transformations.transformations_blur(
        image_id=image_id, current_user=current_user, db=db
    )


@router.patch("/transformations_brown_outline/{image_id}")
async def transformations_brown_outline(
    image_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Apply brown outline transformation to an image.

    :param image_id: The ID of the image.
    :type image_id: int
    :param current_user: The current user. Dependency on auth_service.get_current_user.
    :type current_user: User, optional
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The updated ImageResponse object representing the transformed image.
    :rtype: ImageResponse
    """

    return await repository_transformations.transformations_brown_outline(
        image_id=image_id, current_user=current_user, db=db
    )
