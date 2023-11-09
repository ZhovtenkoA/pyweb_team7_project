from libgravatar import Gravatar
from sqlalchemy.orm import Session

from pyweb_team7_project.database.models import User
from pyweb_team7_project.schemas import UserModel

async def get_user_by_email(email: str, db: Session,) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    then returns the user with that email.
    
    :param email: str: Pass in the email of the user that we want to get
    :param db: Session: Pass the database session to the function
    :return: The first user found with the email specified
    """
    return db.query(User).filter(User.email == email).first()

async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the information to be added to the database.
            db (Session): The SQLAlchemy Session object used for querying and updating data in the database.
        Returns:
            User: A User object representing a newly created user.
    
    :param body: UserModel: Pass the data from the request body into our create_user function
    :param db: Session: Create a database session
    :return: A user object
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.
    
    :param user: User: Identify the user that is being updated
    :param token: str | None: Pass the token to the function
    :param db: Session: Commit the changes to the database
    :return: None, so the return type should be none
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function sets the confirmed field of a user to True.
    
    :param email: str: Pass the email address of the user to be confirmed
    :param db: Session: Pass the database session into the function
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
    