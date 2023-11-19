import os
import sys
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app
from pyweb_team7_project.database.models import Base, User, Image
from pyweb_team7_project.database.db import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    # Create the database

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    except DatabaseError:  # noqa
        db.rollback()
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    return {"username": "testuser", "email": "test@gmail.com", "password": "11223344"}


@pytest.fixture(scope="module")
def comment():
    return {
        "id": 1,
        "user_id": 0,
        "image_id": 0,
        "content": "test comment",
        "created_at": "2023-11-17T22:22:53.247Z",
        "edited_at": "2023-11-17T22:22:53.247Z",
    }


@pytest.fixture(scope="module")
def image():
    mock_image = Image()
    mock_image.id = 0
    mock_image.file_url = "some_url"
    mock_image.description = "image test description"
    mock_image.user_id = 0

    return mock_image

    # return {"id": 0,
    #         "file_url": "some_url",
    #         "description": "image test description",
    #         "user_id": 0
    #         }


@pytest.fixture()
def token(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("pyweb_team7_project.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)

    # current_user = select(User).where(User.email == user.get("email"))

    session = TestingSessionLocal()

    sq = select(User).filter_by(email=user.get("email"))
    result = session.execute(sq)
    current_user = result.scalar_one_or_none()

    current_user.confirmed = True

    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()

    # print(data)
    return data["access_token"]
