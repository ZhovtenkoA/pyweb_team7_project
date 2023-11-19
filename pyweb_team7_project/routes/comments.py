from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from pyweb_team7_project.database.db import get_db
from pyweb_team7_project.database.models import User, Role
from pyweb_team7_project.repository import comments as comments_repo
from pyweb_team7_project.schemas import (
    CommentResponseModel,
    CommentRequestModel,
    CommentUpdateModel,
)
from pyweb_team7_project.services.auth import auth_service
from pyweb_team7_project.services.roles import admin_moderator, admin, free_access

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get(
    "/{comment_id}",
    response_model=CommentResponseModel,
    dependencies=[Depends(free_access)],
)
async def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    """
    Get a comment by its ID.

    :param comment_id: The ID of the comment.
    :param db: The database session used to interact with the database.
    :return: The comment object.
    :raises HTTPException: If the comment with the specified ID does not exist.
    """
    comment_result = await comments_repo.get_comment_by_id(comment_id=comment_id, db=db)
    if comment_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id={comment_id} does not exist!",
        )
    return comment_result


@router.get(
    "/for_image/{image_id}",
    response_model=List[CommentResponseModel],
    dependencies=[Depends(free_access)],
)
async def get_all_image_comments(
    image_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)
):
    """
    Get all comments for a specific image.

    :param image_id: The ID of the image.
    :param skip: The number of comments to skip.
    :param limit: The maximum number of comments to retrieve.
    :param db: The database session used to interact with the database.
    :return: A list of comment objects.
    """
    comments_result = await comments_repo.get_all_image_comments(
        image_id=image_id, skip=skip, limit=limit, db=db
    )
    return comments_result


@router.post(
    "/",
    response_model=CommentResponseModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(free_access)],
)
async def create_comment(
    body: CommentRequestModel,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new comment.

    :param body: The request body containing the comment data.
    :param user: The current authenticated user.
    :param db: The database session used to interact with the database.
    :return: The created comment object.
    :raises HTTPException: If the image with the specified ID does not exist.
    """
    image_db = await comments_repo.get_image_by_id(image_id=body.image_id, db=db)

    if not image_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id={body.image_id} does not exist!",
        )

    created_comment = await comments_repo.create_comment(
        body=body, user=user, image_db=image_db, db=db
    )

    return created_comment


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(admin_moderator)],
)
async def remove_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    Remove a comment by its ID.

    :param comment_id: The ID of the comment.
    :param db: The database session used to interact with the database.
    :param user: The current authenticated user.
    :raises HTTPException: If the comment with the specified ID does not exist.
    """
    comment_db = await comments_repo.get_comment_by_id(comment_id=comment_id, db=db)

    if comment_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id={comment_id} does not exist!",
        )

    comment_db = await comments_repo.remove_comment(comment_db=comment_db, db=db)

    return comment_db


@router.put(
    "/{comment_id}", response_model=CommentResponseModel, dependencies=[Depends(admin)]
)
async def update_comment(
    comment_id: int,
    body: CommentUpdateModel,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    Update a comment by its ID.

    :param comment_id: The ID of the comment.
    :param body: The request body containing the updated comment data.
    :param db: The database session used to interact with the database.
    :param user: The current authenticated user.
    :return: The updated comment object.
    :raises HTTPException: If the comment with the specified ID does not exist or the user does not have permission
                           to edit the comment.
    """
    comment_db = await comments_repo.get_comment_by_id(comment_id=comment_id, db=db)
    if comment_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id={comment_id} does not exist!",
        )

    if comment_db.user_id != user.id and user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit this " "comment",
        )

    comment_db = await comments_repo.update_comment(comment_db, body, db)

    return comment_db
