import unittest
from unittest.mock import patch, MagicMock
import io
import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from pyweb_team7_project.routes import images
from pyweb_team7_project.database.models import User, Image
from pyweb_team7_project.repository.images import create_image_and_upload_to_cloudinary, get_image_by_id, get_all_images, delete_image
from pyweb_team7_project.routes.images import transformations_grayscale, transformations_auto_color, transformations_sepia, transformations_blur, transformations_brown_outline
from pyweb_team7_project.schemas import ImageResponse
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
import fastapi

class ImagesTest(unittest.IsolatedAsyncioTestCase):
    @patch("pyweb_team7_project.repository.images")
    @patch("pyweb_team7_project.services.auth.auth_service")
    @patch("pyweb_team7_project.database.db.get_db")
    async def test_create_image(
        self, mock_get_db, mock_auth_service, mock_repository_images
    ):
        mock_db = MagicMock(spec=Session)
        mock_current_user = MagicMock(spec=User)
        mock_file = MagicMock(spec=UploadFile)
        mock_response = MagicMock(spec=Image)

        mock_get_db.return_value = mock_db
        mock_auth_service.get_current_user.return_value = mock_current_user
        mock_repository_images.create_image_and_upload_to_cloudinary.return_value = mock_response
        description = "Test description"
        user_id = 1
        tag_names = 'tag1, tag2'
        file_url = 'https://example.com/image1.jpg'
        image = Image(description=description, user_id=user_id, file_url = file_url)
        test_image_path = os.path.join(
            os.path.dirname(__file__), "test_images", "test1.jpg"
        )
        with open(test_image_path, "rb") as f:
            file_data = f.read()
        file = UploadFile(filename="test1.jpg", file=io.BytesIO(file_data))

        result = await images.create_image(
            description=description,
            tags=tag_names,
            file=file,
            current_user=mock_current_user,
            db=mock_db,
        )

        self.assertTrue(result.file_url.startswith("https://"))
        self.assertIsInstance(result, Image)
        self.assertEqual(result.description, description)
        # self.assertEqual(result.user_id, user_id)
        self.assertIsNotNone(result.file_url)
        # self.assertEqual(result, image)


    # @patch("pyweb_team7_project.repository.images")
    # @patch("pyweb_team7_project.services.auth.auth_service")
    # @patch("pyweb_team7_project.database.db.get_db")
    # async def test_create_image_with_edge_cases(
    #     self, mock_get_db, mock_auth_service, mock_repository_images
    # ):
    #     # Test case with edge cases
    #     mock_db = MagicMock(spec=Session)
    #     mock_current_user = MagicMock(spec=User)
    #     mock_file = MagicMock(spec=UploadFile)
    #     mock_response = MagicMock(spec=Image)

    #     mock_get_db.return_value = mock_db
    #     mock_auth_service.get_current_user.return_value = mock_current_user
    #     mock_repository_images.create_image_and_upload_to_cloudinary.return_value = mock_response

    #     description = "A"  # Maximum length description
    #     tags = "tag1, " + "tag2," * 1000  # Maximum number of tags
    #     try:
    #         result = await images.create_image(
    #             description=description,
    #             tags=tags,
    #             file=mock_file,
    #             current_user=mock_current_user,
    #             db=mock_db,
    #         )
    #     except fastapi.exceptions.HTTPException as e:
    #     # Проверка соответствующей ошибки
    #         assert e.status_code == 400
    #         assert e.detail == "You can't add more than 5 tags to a photo."

    #     mock_repository_images.create_image_and_upload_to_cloudinary.assert_called_once_with(
    #         mock_db,
    #         mock_file,
    #         description=description,
    #         user_id=mock_current_user.id,
    #         tag_names=["tag1"] + ["tag2"] * 999,
    #     )
    #     self.assertEqual(result, mock_response)


    # @patch("pyweb_team7_project.repository.images")
    # @patch("pyweb_team7_project.services.auth.auth_service")
    # @patch("pyweb_team7_project.database.db.get_db")
    # async def test_create_image_with_exception(
    #     self, mock_get_db, mock_auth_service, mock_repository_images
    # ):
    #     mock_db = MagicMock(spec=Session)
    #     mock_current_user = MagicMock(spec=User)
    #     mock_file = MagicMock(spec=UploadFile)

    #     mock_get_db.return_value = mock_db
    #     mock_auth_service.get_current_user.return_value = mock_current_user
    #     mock_repository_images.create_image_and_upload_to_cloudinary.side_effect = Exception("Test exception")

    #     description = "Test description"
    #     tags = "tag1, tag2"
    #     file = MagicMock(spec=UploadFile)

    #     result = await images.create_image(
    #         description=description,
    #         tags=tags,
    #         file=file,
    #         current_user=mock_current_user,
    #         db=mock_db,
    #     )

    #     mock_repository_images.create_image_and_upload_to_cloudinary.assert_called_once_with(
    #         mock_db,
    #         file,
    #         description=description,
    #         user_id=mock_current_user.id,
    #         tag_names=["tag1", "tag2"],
    #     )
    #     self.assertIsNone(result)

    # @patch("pyweb_team7_project.repository.images")
    # @patch("pyweb_team7_project.services.auth.auth_service")
    # @patch("pyweb_team7_project.database.db.get_db")
    # async def test_create_image_with_none_response(
    #     self, mock_get_db, mock_auth_service, mock_repository_images
    # ):
    #     mock_db = MagicMock(spec=Session)
    #     mock_current_user = MagicMock(spec=User)
    #     mock_file = MagicMock(spec=UploadFile)

    #     mock_get_db.return_value = mock_db
    #     mock_auth_service.get_current_user.return_value = mock_current_user
    #     mock_repository_images.create_image_and_upload_to_cloudinary.return_value = None

    #     description = "Test description"
    #     tags = "tag1, tag2"
    #     file = MagicMock(spec=UploadFile)

    #     result = await images.create_image(
    #         description=description,
    #         tags=tags,
    #         file=file,
    #         current_user=mock_current_user,
    #         db=mock_db,
    #     )

    #     mock_repository_images.create_image_and_upload_to_cloudinary.assert_called_once_with(
    #         mock_db,
    #         file,
    #         description=description,
    #         user_id=mock_current_user.id,
    #         tag_names=["tag1", "tag2"],
    #     )
    #     self.assertIsNone(result)

    # @patch("pyweb_team7_project.repository.images.get_image_by_id")
    # async def test_get_image_with_valid_id(self, mock_get_image_by_id):
    #     mock_db = MagicMock(spec=Session)
    #     mock_current_user = MagicMock(spec=User)
    #     image_id = 1
    #     mock_image = MagicMock(spec=ImageResponse)
    #     mock_get_image_by_id.return_value = mock_image

    #     result = get_image_by_id(
    #         image_id=image_id,
    #         user=mock_current_user,
    #         db=mock_db,
    #     )

    #     mock_get_image_by_id.assert_called_once_with(
    #         mock_current_user, mock_db, image_id
    #     )
    #     self.assertEqual(result, mock_image)

    # @patch("pyweb_team7_project.repository.images.get_image_by_id")
    # async def test_get_image_with_invalid_id(self, mock_get_image_by_id):
    #     mock_db = MagicMock(spec=Session)
    #     mock_current_user = MagicMock(spec=User)
    #     image_id = None
    #     mock_get_image_by_id.return_value = None

    #     try:
    #         get_image_by_id(
    #             image_id=image_id,
    #             user=mock_current_user,
    #             db=mock_db,
    #         )
            
    #         self.fail("HTTPException not raised")
    #     except HTTPException as e:
    #         self.assertEqual(e.status_code, status.HTTP_404_NOT_FOUND)
    #         self.assertEqual(e.detail, "Image not found")

    #     mock_get_image_by_id.assert_called_once_with(
    #         mock_current_user, mock_db, image_id
    #     )

    # @patch("pyweb_team7_project.repository.images.get_image_by_idd")
    # @patch("pyweb_team7_project.repository.images.delete_image")
    # async def test_delete_image_with_valid_id(self, mock_delete_image, mock_get_image_by_id):
    #     mock_db = MagicMock()
    #     mock_current_user = MagicMock()
    #     image_id = 1
    #     mock_image = MagicMock()
    #     mock_get_image_by_id.return_value = mock_image

    #     result = await delete_image(
    #         image_id=image_id,
    #         current_user=mock_current_user,
    #         db=mock_db,
    #     )

    #     mock_get_image_by_id.assert_called_once_with(
    #         user=mock_current_user, image_id=image_id, db=mock_db
    #     )
    #     mock_delete_image.assert_called_once_with(
    #         current_user=mock_current_user, db=mock_db, image_id=image_id
    #     )
    #     self.assertEqual(result, mock_image)

    # @patch("pyweb_team7_project.api.routes.images.repository_images.get_image_by_id")
    # async def test_delete_image_with_invalid_id(self, mock_get_image_by_id):
    #     mock_db = MagicMock()
    #     mock_current_user = MagicMock()
    #     image_id = None
    #     mock_get_image_by_id.return_value = None

    #     try:
    #         await delete_image(
    #             image_id=image_id,
    #             current_user=mock_current_user,
    #             db=mock_db,
    #         )
    #         self.fail("HTTPException not raised")
    #     except HTTPException as e:
    #         self.assertEqual(e.status_code, status.HTTP_404_NOT_FOUND)
    #         self.assertEqual(e.detail, "Image not found")

    #     mock_get_image_by_id.assert_called_once_with(
    #         user=mock_current_user, image_id=image_id, db=mock_db
        # )
   
class TestTransformationsAutoColor(unittest.TestCase):

    @patch('pyweb_team7_project.repository.transformations.cloudinary.config')
    @patch('pyweb_team7_project.repository.transformations.cloudinary.CloudinaryImage.image')
    async def test_transformations_grayscale(self, mock_image, mock_config):
        # Створюємо тестовий об'єкт Image
        test_image = Image(id=1, public_id='test_public_id', user_id=1)
        test_image.fileurl = 'test_url'
        
        # Створюємо mock-об'єкти для db і current_user
        mock_db = MagicMock()
        mock_current_user = MagicMock()

        # Встановлюємо поведінку mock-об'єктів
        mock_db.query().filter().first.return_value = test_image
        mock_image.return_value = 'Transformed HTML string'

        # Викликаємо функцію
        result_image = asyncio.run(transformations_auto_color(1, mock_current_user, mock_db))

        # Перевіряємо, чи були викликані необхідні методи
        mock_db.query().filter().first.assert_called_once_with()
        mock_image.assert_called_once_with(effect="auto_color")

        # Перевіряємо, чи правильно оновлено результат
        self.assertEqual(result_image.fileurl, 'Transformed URL')

        # Перевіряємо, чи правильно викликано методи db
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(test_image)

class TestTransformationsGrayscale(unittest.TestCase):

    @patch('pyweb_team7_project.repository.transformations.cloudinary.config')
    @patch('pyweb_team7_project.repository.transformations.cloudinary.CloudinaryImage.image')
    async def test_transformations_grayscale(self, mock_image, mock_config):
        # Створюємо тестовий об'єкт Image
        test_image = Image(id=1, public_id='test_public_id', user_id=1)
        test_image.fileurl = 'test_url'
        
        # Створюємо mock-об'єкти для db і current_user
        mock_db = MagicMock()
        mock_current_user = MagicMock()

        # Встановлюємо поведінку mock-об'єктів
        mock_db.query().filter().first.return_value = test_image
        mock_image.return_value = 'Transformed HTML string'

        # Викликаємо функцію
        result_image = asyncio.run(transformations_grayscale(1, mock_current_user, mock_db))

        # Перевіряємо, чи були викликані необхідні методи
        mock_db.query().filter().first.assert_called_once_with()
        mock_image.assert_called_once_with(effect="grayscale")

        # Перевіряємо, чи правильно оновлено результат
        self.assertEqual(result_image.fileurl, 'Transformed URL')

        # Перевіряємо, чи правильно викликано методи db
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(test_image)

class TestTransformationsSepia(unittest.TestCase):

    @patch('pyweb_team7_project.repository.transformations.cloudinary.config')
    @patch('pyweb_team7_project.repository.transformations.cloudinary.CloudinaryImage.image')
    async def transformations_sepia(self, mock_image, mock_config):
        # Створюємо тестовий об'єкт Image
        test_image = Image(id=1, public_id='test_public_id', user_id=1)
        test_image.fileurl = 'test_url'
        
        # Створюємо mock-об'єкти для db і current_user
        mock_db = MagicMock()
        mock_current_user = MagicMock()

        # Встановлюємо поведінку mock-об'єктів
        mock_db.query().filter().first.return_value = test_image
        mock_image.return_value = 'Transformed HTML string'

        # Викликаємо функцію
        result_image = asyncio.run(transformations_sepia(1, mock_current_user, mock_db))

        # Перевіряємо, чи були викликані необхідні методи
        mock_db.query().filter().first.assert_called_once_with()
        mock_image.assert_called_once_with(effect="sepia")

        # Перевіряємо, чи правильно оновлено результат
        self.assertEqual(result_image.fileurl, 'Transformed URL')

        # Перевіряємо, чи правильно викликано методи db
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(test_image)

class TestTransformationsBlur(unittest.TestCase):

    @patch('pyweb_team7_project.repository.transformations.cloudinary.config')
    @patch('pyweb_team7_project.repository.transformations.cloudinary.CloudinaryImage.image')
    async def transformations_blur(self, mock_image, mock_config):
        # Створюємо тестовий об'єкт Image
        test_image = Image(id=1, public_id='test_public_id', user_id=1)
        test_image.fileurl = 'test_url'
        
        # Створюємо mock-об'єкти для db і current_user
        mock_db = MagicMock()
        mock_current_user = MagicMock()

        # Встановлюємо поведінку mock-об'єктів
        mock_db.query().filter().first.return_value = test_image
        mock_image.return_value = 'Transformed HTML string'

        # Викликаємо функцію
        result_image = asyncio.run(transformations_blur(1, mock_current_user, mock_db))

        # Перевіряємо, чи були викликані необхідні методи
        mock_db.query().filter().first.assert_called_once_with()
        mock_image.assert_called_once_with(effect="blur:300")

        # Перевіряємо, чи правильно оновлено результат
        self.assertEqual(result_image.fileurl, 'Transformed URL')

        # Перевіряємо, чи правильно викликано методи db
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(test_image)

class TestTransformationsBrownOutline(unittest.IsolatedAsyncioTestCase):

    @patch('pyweb_team7_project.repository.transformations.cloudinary.config')
    @patch('pyweb_team7_project.repository.transformations.cloudinary.CloudinaryImage.image')
    async def transformations_brown_outline(self, mock_image, mock_config):
        # Створюємо тестовий об'єкт Image
        test_image = Image(id=1, public_id='test_public_id', user_id=1)
        test_image.fileurl = 'test_url'
        
        # Створюємо mock-об'єкти для db і current_user
        mock_db = MagicMock()
        mock_current_user = MagicMock()

        # Встановлюємо поведінку mock-об'єктів
        mock_db.query().filter().first.return_value = test_image
        mock_image.return_value = 'Transformed HTML string'

        # Викликаємо функцію
        result_image = asyncio.run(transformations_brown_outline(1, mock_current_user, mock_db))

        # Перевіряємо, чи були викликані необхідні методи
        mock_db.query().filter().first.assert_called_once_with()
        mock_image.assert_called_once_with(effect="co_brown,e_outline")

        # Перевіряємо, чи правильно оновлено результат
        self.assertEqual(result_image.fileurl, 'Transformed URL')

        # Перевіряємо, чи правильно викликано методи db
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(test_image)

if __name__ == "__main__":
    unittest.main()