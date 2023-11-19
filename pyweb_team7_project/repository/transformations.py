from sqlalchemy import and_
from sqlalchemy.orm import Session
import cloudinary

from pyweb_team7_project.database.models import User, Image
from pyweb_team7_project.conf.config import settings


async def transformations_grayscale(
    image_id: int, current_user: User, db: Session
) -> Image:
    """
    Apply grayscale transformation to an image.

    :param image_id: The ID of the image.
    :param current_user: The current authenticated user.
    :param db: The database session used to interact with the database.
    :return: The updated image object.
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

    image.fileurl = image_url
    db.commit()
    db.refresh(image)
    return image


async def transformations_auto_color(
    image_id: int, current_user: User, db: Session
) -> Image:
    """
    Apply auto color transformation to an image.

    :param image_id: The ID of the image.
    :param current_user: The current authenticated user.
    :param db: The database session used to interact with the database.
    :return: The updated image object.
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

    image.fileurl = image_url
    db.commit()
    db.refresh(image)
    return image


async def transformations_sepia(
    image_id: int, current_user: User, db: Session
) -> Image:
    """
    Apply sepia transformation to an image.

    :param image_id: The ID of the image.
    :param current_user: The current authenticated user.
    :param db: The database session used to interact with the database.
    :return: The updated image object.
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

    image.fileurl = image_url
    db.commit()
    db.refresh(image)
    return image


async def transformations_blur(image_id: int, current_user: User, db: Session) -> Image:
    """
    Apply blur transformation to an image.

    :param image_id: The ID of the image.
    :param current_user: The current authenticated user.
    :param db: The database session used to interact with the database.
    :return: The updated image object.
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


async def transformations_brown_outline(
    image_id: int, current_user: User, db: Session
) -> Image:
    """
    Apply brown outline transformation to an image.

    :param image_id: The ID of the image.
    :param current_user: The current authenticated user.
    :param db: The database session used to interact with the database.
    :return: The updated image object.
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

    image.fileurl = image_url
    db.commit()
    db.refresh(image)
    return image
