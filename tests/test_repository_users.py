import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from pyweb_team7_project.database.models import User, Role
from pyweb_team7_project.schemas import UserModel
from pyweb_team7_project.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    get_users,
    make_user_role)


class TestUserFunctions(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email_found(self):
        email = "test@example.com"
        user_mock = MagicMock(spec=User)
        self.session.query(User).filter(User.email == email).first.return_value = user_mock
        result = await get_user_by_email(email=email, db=self.session)
        self.assertEqual(result, user_mock)

    async def test_get_user_by_email_not_found(self):
        user_email = "nonexistent@example.com"
        self.session.query(User).filter(User.email == user_email).first.return_value = None
        result = await get_user_by_email(email=user_email, db=self.session)
        self.assertIsNone(result)

    @patch('libgravatar.Gravatar.get_image')
    async def test_create_user(self, mock_gravatar_get_image):
        user_model = UserModel(email="test@example.com", password="password")
        mock_gravatar_get_image.return_value = "mocked_avatar_url"

        result = await create_user(body=user_model, db=self.session)

        self.assertIsInstance(result, User)
        self.assertEqual(result.email, user_model.email)
        self.assertEqual(result.avatar, "mocked_avatar_url")
        self.assertEqual(result.role, Role.user)

    async def test_update_token(self):
        user_mock = MagicMock(spec=User)
        token = "new_token"
        await update_token(user=user_mock, token=token, db=self.session)
        self.assertEqual(user_mock.refresh_token, token)
        self.session.commit.assert_called_once()

    async def test_confirmed_email(self):
        user_mock = MagicMock(spec=User)
        email = "test@example.com"
        self.session.query().filter().first.return_value = user_mock
        await confirmed_email(email=email, db=self.session)
        self.assertTrue(user_mock.confirmed)
        self.session.commit.assert_called_once()

    async def test_get_users(self):
        skip = 0
        limit = 10
        users_mock = [MagicMock(spec=User), MagicMock(spec=User)]
        self.session.query(User).offset(skip).limit(limit).all.return_value = users_mock
        result = await get_users(skip=skip, limit=limit, db=self.session)
        self.assertEqual(result, users_mock)

    async def test_make_user_role(self):
        email = "test@example.com"
        role = Role.admin
        user_mock = MagicMock(spec=User)
        self.session.query().filter().first.return_value = user_mock

        await make_user_role(email=email, role=role, db=self.session)

        self.assertEqual(user_mock.role, role)
        self.session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()

