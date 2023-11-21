import unittest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from pyweb_team7_project.services.auth import Auth
from jose import JWTError, jwt

class AuthTest(unittest.TestCase):

    def setUp(self):
        self.auth = Auth()

    def test_verify_password(self):
        plain_password = "password123"
        hashed_password = self.auth.get_password_hash(plain_password)
        result = self.auth.verify_password(plain_password, hashed_password)
        self.assertTrue(result)

    def test_get_password_hash(self):
        password = "password123"
        hashed_password = self.auth.get_password_hash(password)
        self.assertTrue(hashed_password)

    def test_create_access_token(self):
        data = {"sub": "user@example.com"}
        expires_delta = 3600
        token = self.auth.create_access_token(data, expires_delta)
        self.assertTrue(token)

    def test_create_refresh_token(self):
        data = {"sub": "user@example.com"}
        expires_delta = 604800
        token = self.auth.create_refresh_token(data, expires_delta)
        self.assertTrue(token)

    @patch("pyweb_team7_project.services.auth.jwt")
    async def test_decode_refresh_token_valid_scope(self, mock_jwt):
        refresh_token = "valid_refresh_token"
        payload = {"scope": "refresh_token", "sub": "user@example.com"}
        self.auth.SECRET_KEY = "secret"
        self.auth.ALGORITHM = "HS256"
        mock_jwt.decode.return_value = payload
        result = self.auth.decode_refresh_token(refresh_token)
        self.assertEqual(result, "user@example.com")

    @patch("pyweb_team7_project.services.auth.jwt")
    async def test_decode_refresh_token_invalid_scope(self, mock_jwt):
        refresh_token = "invalid_refresh_token"
        payload = {"scope": "access_token", "sub": "user@example.com"}
        self.auth.SECRET_KEY = "secret"
        self.auth.ALGORITHM = "HS256"
        mock_jwt.jwt.decode = MagicMock(return_value=payload)
        with self.assertRaises(HTTPException) as context:
            self.auth.decode_refresh_token(refresh_token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid scope for token")

    @patch("pyweb_team7_project.services.auth.jwt")
    async def test_get_current_user_valid_token(self, mock_jwt):
        token = "valid_access_token"
        email = "user@example.com"
        user = MagicMock()
        self.auth.SECRET_KEY = "secret"
        self.auth.ALGORITHM = "HS256"
        mock_jwt.jwt.decode = MagicMock(return_value={"scope": "access_token", "sub": email})
        self.auth.repository_users.get_user_by_email = MagicMock(return_value=user)
        result = self.auth.get_current_user(token)
        self.assertEqual(result, user)

    @patch("pyweb_team7_project.services.auth.jwt")
    async def test_get_current_user_invalid_token(self, mock_jwt):
        token = "invalid_access_token"
        self.auth.SECRET_KEY = "secret"
        self.auth.ALGORITHM = "HS256"
        mock_jwt.jwt.decode = MagicMock(side_effect=self.auth.jwt.JWTError)
        with self.assertRaises(HTTPException) as context:
            self.auth.get_current_user(token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Could not validate credentials")

    def test_create_email_token(self):
        data = {"sub": "user@example.com"}
        token = self.auth.create_email_token(data)
        self.assertTrue(token)

    @patch("pyweb_team7_project.services.auth.jwt")
    async def test_get_email_from_token(self, mock_jwt):
        token = "valid_token"
        email = "user@example.com"
        self.auth.SECRET_KEY = "secret"
        self.auth.ALGORITHM = "HS256"
        mock_jwt.jwt.decode = MagicMock(return_value={"sub": email})
        result = self.auth.get_email_from_token(token)
        self.assertEqual(result, email)

if __name__ == "main":
    unittest.main()