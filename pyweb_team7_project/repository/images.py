from sqlalchemy import and_
from sqlalchemy.orm import Session

import cloudinary

from pyweb_team7_project.database.models import User, Image, Tag
from pyweb_team7_project.conf.config import settings

# async def create_image(db: Session, fileurl: str, public_id: str, description: str, user_id: int, tag_names: list = None) -> Image:
#     """
#     The create_image function creates a new image in the database.
#         Args:
#             db (Session): The database session to use for this operation.
#             filename (str): The name of the file that contains the image data. This is not stored in the DB, but used by
#              our application to locate and load images from disk when requested by clients.
#             description (str): A short description of what's contained within this image, such as &quot;A picture of my
#             dog&quot; or &quot;The view from my window&quot;. This will be displayed on our web app so users can see what
#             an image is about before they click on it to
#
#     :param db: Session: Access the database
#     :param filename: str: Store the filename of the image
#     :param description: str: Store the description of the image
#     :param user_id: int: Specify the user who created the image
#     :param tag_names: list: Pass in a list of tag names to be added to the image
#     :return: An image object
#     :doc-author: Trelent
#     """
#     user = db.query(User).filter_by(id=user_id).first()
#     if not user:
#         raise Exception("User not found")
#
#     image = Image(fileurl=fileurl, public_id=public_id, description=description, user_id=user_id)
#     if tag_names:
#         for tag_name in tag_names:
#             tag = db.query(Tag).filter_by(name=tag_name).first()
#             if not tag:
#                 tag = Tag(name=tag_name)
#             image.tags.append(tag)
#
#         db.add(image)
#         db.commit()
#         db.refresh(image)
#         return image


async def create_image_and_upload_to_cloudinary(db: Session, file, description: str, user_id: int, tag_names: list = None) -> Image:

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise Exception("User not found")

    image = Image(description=description, user_id=user_id)

    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    cloudinary_response = cloudinary.uploader.upload(file)

    image.file_url = cloudinary_response.get('secure_url')

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
    The get_image_by_id function takes in a user, database session, and image id.
    It then queries the database for an image with that id and returns it.

    :param user: User: Pass the user object to the function
    :param db: Session: Pass the database session to the function
    :param image_id: int: Filter the image by id
    :return: The image object that matches the user and image id
    :doc-author: Trelent
    """
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).first()
    return image


async def update_image_description(user: User, db: Session, image_id: int, new_description: str):
    """
    The update_image_description function updates the description of an image in the database.
        Args:
            user (User): The user who is updating their image's description.
            db (Session): A connection to the database that will be used for querying and committing changes.
            image_id (int): The id of the image whose description is being updated.
            new_description (str): The new description that will replace any previous descriptions for this particular image.

    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :param image_id: int: Identify the image to be updated
    :param new_description: str: Update the description of an image
    :return: The image object, which is then used to update the description
    :doc-author: Trelent
    """
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).first()
    if image:
        image.description = new_description
        db.commit()
    return image


async def delete_image(user: User, db: Session, image_id: int):
    """
    The delete_image function deletes an image from the database.
        Args:
            user (User): The user who is deleting the image.
            db (Session): A connection to the database.  This is used to delete images from it.
            image_id (int): The id of the image that will be deleted.

    :param user: User: Get the user id of the user who is logged in
    :param db: Session: Pass the database session to the function
    :param image_id: int: Identify the image that is to be deleted
    :return: The image that was deleted
    :doc-author: Trelent
    """
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).first()
    if image:
        db.delete(image)
        db.commit()
    return image
