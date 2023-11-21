from typing import List

from sqlalchemy.orm import Session

from pyweb_team7_project.database.models import Comment, User, Image
from pyweb_team7_project.schemas import CommentResponseModel, CommentRequestModel


async def get_comment_by_id(comment_id: int, db: Session) -> Comment | None:
    """
    The get_comment_by_id function takes a comment_id and db as parameters.
    It returns the first Comment object in the database that matches the given comment_id.

    :param comment_id: int: Specify the id of the comment to be returned
    :param db: Session: Pass the database session into the function
    :return: The comment object with the given id
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()

async def get_all_image_comments(
    image_id: int, skip: int, limit: int, db: Session
) -> List[Comment]:
    """
    The get_all_image_comments function returns a list of comments for the image with the given id.
    The skip and limit parameters are used to paginate through results.

    :param image_id: int: Filter the comments by image id
    :param skip: int: Skip a number of comments
    :param limit: int: Limit the number of comments returned
    :param db: Session: Pass the database session to the function
    :return: A list of comments for a given image id
    """
    return (
        db.query(Comment)
        .filter(Comment.image_id == image_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def create_comment(
    body: CommentRequestModel, user: User, image_db: Image, db: Session
) -> CommentResponseModel | None:
    """
    The create_comment function creates a new comment in the database.
        It takes in a CommentRequestModel, which is used to create the new comment.
        The function also takes in an image_db object and user object, which are used to associate the newly created
        comment with an image and user respectively. Finally, it takes in a db session for interacting with the database.

    :param body: CommentRequestModel: Get the content of the comment
    :param user: User: Get the user who is making the comment
    :param image_db: Image: Get the image that is being commented on
    :param db: Session: Create a database session
    :return: A commentresponsemodel
    """
    new_comment = Comment()
    new_comment.content = body.content

    new_comment.user = user
    new_comment.image = image_db
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


async def update_comment(
    comment_db: Comment, body: CommentRequestModel, db: Session
) -> Comment | None:
    """
    The update_comment function updates a comment in the database.
        Args:
            comment_db (Comment): The Comment object to be updated.
            body (CommentRequestModel): The new content of the Comment object.
            db (Session): A Session instance for interacting with the database.

    :param comment_db: Comment: Pass the comment object to the function
    :param body: CommentRequestModel: Get the content of the comment
    :param db: Session: Access the database
    :return: The updated comment
    """
    comment_db.content = body.content
    db.commit()
    db.refresh(comment_db)
    return comment_db


# todo: видаляти коменти можуnь тільки адміни
async def remove_comment(comment_db: Comment, db: Session) -> Comment | None:
    """
    The remove_comment function removes a comment from the database.
    Args:
        comment_db (Comment): The Comment object to be removed from the database.
        db (Session): The Session object used to interact with the database.
    :param comment_db: Comment: The comment object to be deleted.
    :param db: Session: The database session.
    :return: The comment that was deleted or `None` if the comment does not exist.
    """
    db.delete(comment_db)
    db.commit()
    return comment_db
