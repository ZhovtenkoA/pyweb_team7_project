from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from pyweb_team7_project.database.db import get_db
from pyweb_team7_project.database.models import User
from pyweb_team7_project.repository import comments as comments_repo
from pyweb_team7_project.schemas import CommentResponseModel
from pyweb_team7_project.services.auth import auth_service

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/{comment_id}", response_model=CommentResponseModel)
async def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    comment_result = await comments_repo.get_conmment(comment_id, db)
    if comment_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return comment_result


# @router.post("/", response_model=CommentResponseModel)
# async def create_comment(comment_id: int, user: User = Depends(auth_service.get_current_user),
#                          db: Session = Depends(get_db)):
#     comment_result = await comments_repo.get_conmment(comment_id, user, db)
#     if comment_result is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
#         )
#     return comment_result

def dsadsad():
    pass