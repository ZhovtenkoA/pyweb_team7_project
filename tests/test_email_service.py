import unittest
from unittest.mock import MagicMock, patch
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from pathlib import Path
from pyweb_team7_project.services.auth import auth_service
from pyweb_team7_project.services.email import send_email


class TestSendEmail(unittest.TestCase):
    @patch('pyweb_team7_project.services.auth.auth_service.create_email_token')
    @patch('fastapi_mail.FastMail')
    async def test_send_email_success(self, mock_fm, mock_create_email_token):
        # Mock the necessary objects and methods
        email = "test@example.com"
        username = "test_user"
        host = "example.com"
        token_verification = "test_token"

        # Configure the mock objects
        mock_create_email_token.return_value = token_verification

        # Call the function being tested
        await send_email(email, username, host)

        # Assertions
        mock_create_email_token.assert_called_once_with({"sub": email})
        mock_fm.assert_called_once_with(ConnectionConfig(
            MAIL_USERNAME="test_mail_username",
            MAIL_PASSWORD="test_mail_password",
            MAIL_FROM="test_mail_from",
            MAIL_PORT="test_mail_port",
            MAIL_SERVER="test_mail_server",
            MAIL_FROM_NAME='John Snow',
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates',
        ))
        mock_fm.return_value.send_message.assert_called_once_with(
            MessageSchema(
                subject="Confirm your email",
                recipients=[email],
                template_body={"host": host, "username": username, "token": token_verification},
                subtype=MessageType.html
            ),
            template_name="email_templates.html"
        )

    @patch('pyweb_team7_project.services.auth.auth_service.create_email_token')
    @patch('fastapi_mail.FastMail')
    async def test_send_email_connection_error(self, mock_fm, mock_create_email_token):
        # Mock the necessary objects and methods
        email = "test@example.com"
        username = "test_user"
        host = "example.com"

        # Configure the mock objects
        mock_create_email_token.side_effect = ConnectionErrors("Mocked connection error")

        # Call the function being tested
        await send_email(email, username, host)

        # Assertions
        mock_create_email_token.assert_called_once_with({"sub": email})
        mock_fm.assert_not_called()

    @patch('pyweb_team7_project.services.auth.auth_service.create_email_token')
    @patch('fastapi_mail.FastMail')
    async def test_send_email_empty_email(self, mock_fm, mock_create_email_token):
        # Mock the necessary objects and methods
        email = ""
        username = "test_user"
        host = "example.com"

        # Call the function being tested
        await send_email(email, username, host)

        # Assertions
        mock_create_email_token.assert_not_called()
        mock_fm.assert_not_called()

    @patch('pyweb_team7_project.services.auth.auth_service.create_email_token')
    @patch('fastapi_mail.FastMail')
    async def test_send_email_invalid_email(self, mock_fm, mock_create_email_token):
        # Mock the necessary objects and methods
        email = "invalid_email"
        username = "test_user"
        host = "example.com"

        # Call the function being tested
        await send_email(email, username, host)

        # Assertions
        mock_create_email_token.assert_not_called()
        mock_fm.assert_not_called()

if __name__ == '__main__':
    unittest.main()