from sqlalchemy.orm import Session

from pyweb_team7_project.database.models import Comment, User, Image
from pyweb_team7_project.schemas import CommentResponseModel, CommentRequestModel


async def get_conmment(comment_id: int, db: Session) -> Comment | None:
    """
    The get_conmment function returns a Comment object from the database.

    :param comment_id: int: Specify the type of the parameter and its name
    :param db: Session: Pass the database session to the function
    :return: The first comment in the database with an id that matches the comment_id argument
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()


async def create_comment(body: CommentRequestModel, user: User, db: Session) -> CommentResponseModel | None:
    """
    The create_comment function creates a new comment in the database.
        Args:
            body (CommentRequestModel): The request model for creating a comment.
            user (User): The current user making the request to create a comment.
            db (Session): A connection to the database that is used for querying and updating data.

    :param body: CommentRequestModel: Get the content of the comment
    :param user: User: Get the user object from the database
    :param db: Session: Access the database
    :return: The new comment object
    """
    image_db = db.query(Image).filter(id=body.image_id).first()

    if image_db:
        new_comment = Comment()
        new_comment.content = body.content

        new_comment.user = user
        new_comment.image = image_db
        db.commit()
        # db.refresh(contact)
        return new_comment


async def update_tag(comment_id: int, body: CommentRequestModel, db: Session) -> Comment | None:
    """
    The update_tag function updates a comment in the database.
        Args:
            comment_id (int): The id of the tag to update.
            body (CommentRequestModel): The updated content for the tag.

    :param comment_id: int: Find the comment in the database
    :param body: CommentRequestModel: Pass the comment data to the function
    :param db: Session: Pass the database session to the function
    :return: The comment object
    """
    comment_db = db.query(Comment).filter(id=comment_id).first()
    if comment_db:
        comment_db.content = body.content
        db.commit()
    return comment_db


# todo: видаляти коменти можуь тільки адміни
async def remove_comment(comment_id: int, db: Session) -> Comment | None:
    """
    The remove_comment function removes a comment from the database.
        Args:
            comment_id (int): The id of the comment to be removed.
            db (Session): A connection to the database.

    :param comment_id: int: Identify the comment to be removed
    :param db: Session: Connect to the database
    :return: The comment that was removed
    """
    comment_db = db.query(Comment).filter(id=comment_id).first()
    # await comment_db = get_conmment(comment_id, db)

    if comment_db:
        db.delete(comment_db)
        db.commit()
    return comment_db
