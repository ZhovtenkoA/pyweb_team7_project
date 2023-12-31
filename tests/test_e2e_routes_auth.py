from unittest.mock import MagicMock

from pyweb_team7_project.database.models import User


def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("pyweb_team7_project.routes.auth.send_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()

    print(data)

    assert "user" in data

    db_user = data["user"]

    assert db_user["email"] == user.get("email")
    assert "id" in db_user
    assert 'username' in db_user 
    assert 'email' in db_user 
    assert 'avatar' in db_user 
    assert 'role' in db_user 


def test_repeat_create_user(client, user):
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 409, response.text
    data = response.json()

    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


def test_login_user(client, session, user):
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_user_wrong_password(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": "password"},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


def test_login_user_wrong_email(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": "testtest@gmail.com", "password": user.get("password")},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"
