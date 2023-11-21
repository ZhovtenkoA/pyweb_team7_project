from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from ..database.db import get_db
from ..database.models import User
from ..repository.images import update_image_qrcode_url, get_image_by_id
from ..schemas import QRCodeResponse, QRCodeRequestTest, ImageResponse
from ..services.auth import auth_service
from ..services.qrcode_generation import get_qrcode_image_url

router = APIRouter(prefix="/qrcode", tags=["QRCode"])


@router.post(
    "/test", response_model=QRCodeResponse, status_code=status.HTTP_201_CREATED
)
async def create_qr_test(
    body: QRCodeRequestTest, user: User = Depends(auth_service.get_current_user)
):
    """
    Create a QR code for testing.

    :param body: The request body containing the QR code data.
    :type body: QRCodeRequestTest
    :param user: The current user. Dependency on auth_service.get_current_user.
    :type user: User, optional
    :return: The QRCodeResponse containing the URL of the generated QR code.
    :rtype: QRCodeResponse
    """
    qr_image_url = await get_qrcode_image_url(
        qr_data=body.qr_data, folder_name=user.username
    )

    return {"qrcode_cloud_url": qr_image_url}


@router.post(
    "/{image_id}", response_model=ImageResponse, status_code=status.HTTP_201_CREATED
)
async def create_image_qrcode(
    image_id: int,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a QR code for an image.

    :param image_id: The ID of the image.
    :type image_id: int
    :param user: The current user. Dependency on auth_service.get_current_user.
    :type user: User, optional
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The updated ImageResponse with the QR code URL.
    :rtype: ImageResponse
    :raises HTTPException 404: If the image with the specified ID does not exist.
    """

    image_db = await get_image_by_id(image_id=image_id, db=db)

    if not image_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id={image_id} does not exist!",
        )

    qr_image_url = await get_qrcode_image_url(
        qr_data=image_db.file_url, folder_name=user.username
    )

    changed_image = await update_image_qrcode_url(
        image=image_db, db=db, new_qrcode_url=qr_image_url
    )

    return changed_image
