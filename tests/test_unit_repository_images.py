import unittest
from unittest.mock import MagicMock, patch
import asyncio
from sqlalchemy.orm import Session
import os
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

class TestCreateImageAndUploadToCloudinary(unittest.TestCase):
    @patch("pyweb_team7_project.routes.images.cloudinary.config")
    @patch("pyweb_team7_project.repository.images.create_image_and_upload_to_cloudinary")
    async def test_create_image_and_upload_to_cloudinary(self, mock_upload, mock_config):
        db_session = MagicMock(spec=Session)
        file_mock = MagicMock()
        file_mock.file = os.path.join(
            os.path.dirname(__file__), "test_images", "test.jpg")
        description = "Test image"
        user_id = 1
        tag_names = ["tag1", "tag2"]

        user = User(id=user_id)
        db_session.query.return_value.filter_by.return_value.first.return_value = user

        mock_upload.return_value = {
            "public_id": "public_id",
            "secure_url": "https://example.com/image.jpg",
        }

        result = create_image_and_upload_to_cloudinary(
            db_session, file_mock, description, user_id, tag_names
        )

        # Проверяем, что функции и методы были вызваны с правильными аргументами
        db_session.query.assert_called_once_with(User)
        db_session.query.return_value.filter_by.assert_called_once_with(id=user_id)
        mock_upload.assert_called_once_with(file_mock.file)

        # Проверяем, что создан объект Image с правильными значениями
        self.assertIsInstance(result, Image)
        self.assertEqual(result.description, description)
        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.file_url, "https://example.com/image.jpg")
        self.assertEqual(result.public_id, "public_id")

        # Проверяем, что были созданы и связаны объекты Tag
        self.assertEqual(len(result.tags), 2)
        self.assertIsInstance(result.tags[0], Tag)
        self.assertEqual(result.tags[0].name, "tag1")
        self.assertIsInstance(result.tags[1], Tag)
        self.assertEqual(result.tags[1].name, "tag2")

        self.assertIsInstance(result, Image)
        self.assertEqual(result.file_url, mock_upload["secure_url"])
        self.assertEqual(result.public_id, mock_upload["public_id"])
        self.assertEqual(result.description, self.description)
        self.assertEqual(result.user_id, self.user.id)
        self.assertEqual(len(result.tags), len(self.tag_names))
        self.assertTrue(all(tag.name in self.tag_names for tag in result.tags))

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
