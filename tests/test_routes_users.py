from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from pyweb_team7_project.database.db import get_db
from pyweb_team7_project.database.models import User, Role
from pyweb_team7_project.schemas import UserDb
from pyweb_team7_project.services.roles import free_access, admin
from pyweb_team7_project.repository import users
from pydantic import EmailStr

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/users/get_all", response_model=list[UserDb], dependencies=[Depends(free_access)])
async def get_all_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    list_users = await users.get_users(skip, limit, db)
    return list_users


@app.patch("/users/assign_role/{role:Role}", dependencies=[Depends(admin)])
async def assign_role(email: EmailStr, role: Role, db: Session = Depends(get_db)):
    user = await users.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if role == user.role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already assigned")

    await users.make_user_role(email, role, db)
    return {"message": f"Role assigned to {email}: {role.value}"}