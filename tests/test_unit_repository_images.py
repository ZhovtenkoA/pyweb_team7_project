import unittest
from unittest.mock import MagicMock, patch
import asyncio
from sqlalchemy.orm import Session
import os
from pyweb_team7_project.conf.config import settings
from pyweb_team7_project.repository.images import (
    create_image_and_upload_to_cloudinary,
    get_image_by_id,
    get_all_images,
    update_image_description,
    update_image_qrcode_url,
    delete_image,
    get_QR,
)
from pyweb_team7_project.database.models import (
    User,
    Image,
    Tag,
    QR_code,
)
from cloudinary import uploader
import cloudinary
import io
from fastapi import HTTPException, status, UploadFile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pyweb_team7_project.database.models import Base
from pyweb_team7_project.database import db

class ImagesTest(unittest.IsolatedAsyncioTestCase):
    @patch("pyweb_team7_project.repository.images")
    @patch("pyweb_team7_project.services.auth.auth_service")
    @patch("pyweb_team7_project.database.db.get_db")
    async def test_create_image_and_upload_to_cloudinary(
        self, mock_get_db, mock_auth_service, mock_repository_images
    ):
        mock_db = MagicMock(spec=Session)
        mock_file = MagicMock(spec=UploadFile)
        mock_image = MagicMock(spec=Image)

        mock_get_db.return_value = mock_db
        mock_repository_images.Image.return_value = mock_image

        description = "Test description"
        user_id = 1
        tag_names = ["tag1", "tag2"]
        file_url = 'https://example.com/image1.jpg'

        image = Image(description=description, user_id=user_id, file_url = file_url)
        test_image_path = os.path.join(
            os.path.dirname(__file__), "test_images", "test1.jpg"
        )
        with open(test_image_path, "rb") as f:
            file_data = f.read()
        file = UploadFile(filename="test1.jpg", file=io.BytesIO(file_data))

        mock_db.query.return_value.filter_by.return_value.first.return_value = MagicMock()

        mock_upload = MagicMock()
        mock_upload.return_value = {
            "public_id": "public_id",
            "secure_url": "https://example.com/image1.jpg",
        }
        with patch("pyweb_team7_project.repository.images.upload", mock_upload):
            result = await create_image_and_upload_to_cloudinary(
                mock_db, file, description, user_id, tag_names
            )
            
        print(result)
        #mock_db.query.assert_called_once_with(User)
        #mock_db.query.return_value.filter_by.assert_called_once_with(id=user_id)
        #mock_repository_images.Image.assert_called_once_with(
            #description=description, user_id=user_id, file_url="cloudinary"
        #)
        #mock_upload.assert_called_once_with(file.file)

        # self.assertEqual(result, mock_image)
        #         # Проверяем, что вызываются ожидаемые методы и функции
        # mock_db.query.assert_called_once_with(User)
        # mock_db.query.return_value.filter_by.assert_called_once_with(id=user_id)
        #mock_upload.assert_called_once_with(str(file_mock))

        self.assertTrue(result.file_url.startswith("https://"))
        self.assertIsInstance(result, Image)
        self.assertEqual(result.description, description)
        self.assertEqual(result.user_id, user_id)
        self.assertIsNotNone(result.file_url)
        # mock_db.close()
    @patch("pyweb_team7_project.repository.images")
    @patch("pyweb_team7_project.services.auth.auth_service")
    @patch("pyweb_team7_project.database.db.get_db")
    async def test_create_image_and_upload_to_cloudinary_no_user(
        self, mock_get_db, mock_auth_service, mock_repository_images
    ):
        mock_db = MagicMock(spec=Session)
        mock_file = MagicMock(spec=UploadFile)
        mock_image = MagicMock(spec=Image)

        mock_get_db.return_value = mock_db
        mock_repository_images.Image.return_value = mock_image

        description = "Test description"
        user_id = 1
        tag_names = ["tag1", "tag2"]
        file_url = 'https://example.com/image1.jpg'

        image = Image(description=description, user_id=user_id, file_url = file_url)
        test_image_path = os.path.join(
            os.path.dirname(__file__), "test_images", "test1.jpg"
        )
        with open(test_image_path, "rb") as f:
            file_data = f.read()
        file = UploadFile(filename="test1.jpg", file=io.BytesIO(file_data))

        mock_db.query.return_value.filter_by.return_value.first.return_value = None  # Установка результата поиска пользователя в None

        mock_upload = MagicMock()
        mock_upload.return_value = {
            "public_id": "public_id",
            "secure_url": "https://example.com/image1.jpg",
        }
        with patch("pyweb_team7_project.repository.images.upload", mock_upload):
            with self.assertRaises(Exception) as context:  # Проверяем, что исключение возникает
                result = await create_image_and_upload_to_cloudinary(
                    mock_db, file, description, user_id, tag_names
                )
        
        self.assertEqual(str(context.exception), "User not found")
class TemporaryFileWrapper:
        def __init__(self, file_path):
            self.file_path = file_path

        @property
        def file(self):
            return open(self.file_path, "rb")
        
class TestImageFunctions(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.file = MagicMock()
        self.file.return_value = b"dummy_file_data"
        self.description = "Test image"
        self.tag_names = ["test", "image"]
        self.cloudinary_upload = {
            "secure_url": "https://example.com/image.jpg",
            "public_id": "public_id",
        }

    def tearDown(self):
        # Clean up data after running tests
        self.session.rollback()


    async def test_get_image_by_id(self):
        image_id = 1
        image = Image(id=image_id, user_id=self.user.id)
        self.session.query().filter().first.return_value = image

        result = await get_image_by_id(
            user=self.user, db=self.session, image_id=image_id
        )

        self.assertEqual(result, image)
        assert isinstance(result, Image)
        assert result.id == image.id
        assert result.description == image.description
        assert result.user_id == image.user_id

    async def test_get_all_images(self):
        images = [Image(id=1, user_id=self.user.id), Image(id=2, user_id=self.user.id)]
        self.session.query().all.return_value = images

        result = await get_all_images(self.session)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(image, Image) for image in result))

    async def test_update_image_description(self):
        image_id = 1
        new_description = "Updated Description"
        existing_image = Image(
            id=image_id, user_id=self.user.id, description="Old Description"
        )
        self.session.query().filter().first.return_value = existing_image

        result = await update_image_description(
            user=self.user,
            db=self.session,
            image_id=image_id,
            new_description=new_description,
        )

        self.assertEqual(result.description, new_description)
        assert isinstance(result, Image)
        assert result.id == existing_image.id
        assert result.description == new_description

    async def test_update_image_qrcode_url(self):
        # Create a dummy image
        image_id = 1
        image = Image(id=image_id)  
        new_qrcode_url = "https://example.com/qr_code.png"
        # Call the function
        updated_image = await update_image_qrcode_url(
            image, self.session, new_qrcode_url
        )

        # Assertions
        self.assertIsInstance(updated_image, Image)
        self.assertEqual(updated_image.id, image_id)
        # self.assertEqual(updated_image.qr_code.url, new_qrcode_url)

    async def test_delete_image(self):
        image_id = 1
        existing_image = Image(id=image_id, user_id=self.user.id)
        self.session.query().filter().first.return_value = existing_image
        result = await delete_image(user=self.user, db=self.session, image_id=image_id)
        self.assertEqual(result, existing_image)
        assert isinstance(result, Image)
        assert result.id == existing_image.id
        assert result.description == existing_image.description
        assert result.user_id ==existing_image.user_id
        assert result.file_url is None

    async def test_delete_image_not_found(self):
        image_id = None
        existing_image = Image(id=image_id, user_id=self.user.id)
        self.session.query().filter().first.return_value = existing_image
        result = await delete_image(user=self.user, db=self.session, image_id=image_id) 
        self.assertEqual(result, existing_image)

    async def test_get_QR(self):
        # Check getting the QR code URL for an image
        image_id = 1
        qr_code = await get_QR(image_id, self.session)
        self.assertIsInstance(qr_code, dict)
        self.assertIn("qr_code_url", qr_code)

if __name__ == "__main__":
    unittest.main()