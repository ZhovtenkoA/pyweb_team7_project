from sqlalchemy import and_
from sqlalchemy.orm import Session

import cloudinary
from cloudinary.uploader import upload

from pyweb_team7_project.database.models import User, Image, Tag, QR_code
from pyweb_team7_project.conf.config import settings

import os
import qrcode
import cloudinary


async def create_image_and_upload_to_cloudinary(
    db: Session, file, description: str, user_id: int, tag_names: list = None
) -> Image:
    """
    Create an image object, upload the image file to Cloudinary, and associate it with a user in the database.

    :param db: The database session used to interact with the database.
    :param file: The image file to be uploaded.
    :param description: The description of the image.
    :param user_id: The ID of the user who owns the image.
    :param tag_names: A list of tag names to associate with the image. Defaults to None.
    :type db: Session
    :type file: Any
    :type description: str
    :type user_id: int
    :type tag_names: list, optional
    :return: The created image object.
    :rtype: Image
    """
    user = db.query(User).filter_by(id=user_id).first()

    if not user:
        raise Exception("User not found")

    image = Image(description=description, user_id=user_id, file_url="cloudinary")

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    print(file.file)

    result = upload(file.file)

    # Отримуємо public ID завантаженого зображення
    image.public_id = result.get("public_id")
    # Отримайте URL обробленого зображення
    image.file_url = result.get("secure_url")

    if tag_names:
        for tag_name in tag_names:
            tag = db.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            image.tags.append(tag)

    db.add(image)
    db.commit()
    db.refresh(image)

    return image


async def get_image_by_id(user: User, db: Session, image_id: int):
    """
    Retrieve an image from the database based on the provided user, database session, and image ID.

    :param user: The user object.
    :param db: The database session used to interact with the database.
    :param image_id: The ID of the image to retrieve.
    :type user: User
    :type db: Session
    :type image_id: int
    :return: The retrieved image object.
    :rtype: Image
    """
    image = (
        db.query(Image)
        .filter(
            and_(
                Image.id == image_id,
                # Image.user_id == user.id
            )
        )
        .first()
    )
    return image


async def get_all_images(db: Session):
    """
    Retrieve all images from the database.

    :param db: The database session used to interact with the database.
    :type db: Session
    :return: A list of all image objects.
    :rtype: List[Image]
    """
    images = db.query(Image).all()
    return images


async def update_image_description(
    user: User, db: Session, image_id: int, new_description: str
):
    """
    Update the description of an image in the database.

    :param user: The user object who is updating the image description.
    :param db: The database session used to interact with the database.
    :param image_id: The ID of the image to update.
    :param new_description: The new description for the image.
    :type user: User
    :type db: Session
    :type image_id: int
    :type new_description: str
    :return: The updated image object.
    :rtype: Image
    """
    image = (
        db.query(Image)
        .filter(
            and_(
                Image.id == image_id,
                # Image.user_id == user.id
            )
        )
        .first()
    )
    if image:
        image.description = new_description
        db.commit()
    return image


async def update_image_qrcode_url(image: Image, db: Session, new_qrcode_url: str):
    """
    Update the QR code URL of an image in the database.

    :param image: The image object to update.
    :param db: The database session used to interact with the database.
    :param new_qrcode_url: The new QR code URL for the image.
    :type image: Image
    :type db: Session
    :type new_qrcode_url: str
    :return: The updated image object.
    :rtype: Image
    """
    if image:
        # image.qrcode_url = new_qrcode_url
        image.file_url = new_qrcode_url
        db.commit()
        db.refresh(image)
        return image


async def delete_image(user: User, db: Session, image_id: int):
    """
    Delete an image from the database.

    :param user: The user object who is deleting the image.
    :param db: The database session used to interact with the database.
    :param image_id: The ID of the image to delete.
    :type user: User
    :type db: Session
    :type image_id: int
    :return: The deleted image object.
    :rtype: Image
    """
    image = (
        db.query(Image)
        .filter(and_(Image.id == image_id, Image.user_id == user.id))
        .first()
    )
    if not image:
        return False, {"message": "image not found"}
    if image:
        # Delete corresponding qr_codes rows
        db.query(QR_code).filter(QR_code.photo_id == image_id).delete()
        db.delete(image)
        db.commit()
        print("Image deleted")
    return image


async def get_QR(image_id: int, db: Session):
    """
    Retrieve the QR code URL for an image from the database.

    :param image_id: The ID of the image.
    :param db: The database session used to interact with the database.
    :type image_id: int
    :type db: Session
    :return: A dictionary containing the QR code URL for the image.
    :rtype: Dict[str, str]
    """
    image = db.query(Image).filter(and_(Image.id == image_id)).first()
    if image is None:
        raise Exception("Image not found")
    else:
        qr = db.query(QR_code).filter(and_(QR_code.photo_id == image_id)).first()
        print(qr)
        if qr is None:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            print("qr data")
            qr.add_data(image.file_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            qr_code_file_path = "my_qr_code.png"
            img.save(qr_code_file_path)

            cloudinary.config(
                cloud_name=settings.cloudinary_name,
                api_key=settings.cloudinary_api_key,
                api_secret=settings.cloudinary_api_secret,
                secure=True,
            )

            upload_result = cloudinary.uploader.upload(
                qr_code_file_path,
                public_id=f"Qr_Code/Photo_{image_id}",
                overwrite=True,
                invalidate=True,
            )
            qr = QR_code(url=upload_result["secure_url"], photo_id=image_id)

            try:
                db.add(qr)
                db.commit()
                db.refresh(qr)
            except Exception as e:
                await db.rollback()
                raise e

            os.remove(qr_code_file_path)
            return {"qr_code_url": qr.url}

        return {"qr_code_url": qr}
