import unittest
from unittest.mock import patch, MagicMock
from unittest import mock
import io
import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from pyweb_team7_project.routes import images
from pyweb_team7_project.database.models import User, Image, Role
from pyweb_team7_project.repository.images import get_all_images
from pyweb_team7_project.routes.images import transformations_grayscale, transformations_auto_color, transformations_sepia, transformations_blur, transformations_brown_outline, get_image, delete_image, update_image
from pyweb_team7_project.schemas import ImageResponse, UpdateImageModel
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
import fastapi
import pytest
from fastapi.testclient import TestClient
from main import app
from fastapi_limiter import FastAPILimiter
from starlette import status as starlette_status
client = TestClient(app)

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


    @patch("pyweb_team7_project.repository.images")
    @patch("pyweb_team7_project.services.auth.auth_service")
    @patch("pyweb_team7_project.database.db.get_db")
    async def test_create_image_with_edge_cases(
        self, mock_get_db, mock_auth_service, mock_repository_images
    ):
        # Test case with edge cases
        mock_db = MagicMock(spec=Session)
        mock_current_user = MagicMock(spec=User)
        mock_file = MagicMock(spec=UploadFile)
        mock_response = MagicMock(spec=Image)
        test_image_path = os.path.join(
            os.path.dirname(__file__), "test_images", "test1.jpg"
        )
        with open(test_image_path, "rb") as f:
            file_data = f.read()
        file = UploadFile(filename="test1.jpg", file=io.BytesIO(file_data))
        mock_get_db.return_value = mock_db
        mock_auth_service.get_current_user.return_value = mock_current_user
        mock_repository_images.create_image_and_upload_to_cloudinary.return_value = mock_response

        description = "description"
        tags = "verylongdescriptionofimagesandtags"
        with pytest.raises(fastapi.exceptions.HTTPException) as e:
            await images.create_image(
                description=description,
                tags=tags,
                file=file,
                current_user=mock_current_user,
                db=mock_db,
            )
        assert e.value.status_code == 400
        assert e.value.detail == "Tag name should be no more than 25 characters long."

    @patch("pyweb_team7_project.repository.images.get_image_by_id")
    @patch("pyweb_team7_project.database.db.get_db")
    async def test_get_image_with_valid_id(self, mock_get_db, mock_get_image_by_id):
        mock_db = MagicMock(spec=Session)
        mock_current_user = MagicMock(spec=User)
        description = "Test description"
        user_id = 1
        image_id = 1
        tag_names = ['tag1', 'tag2']
        file_url = 'https://example.com/image1.jpg'
        image = Image(id=image_id, description=description, user_id=user_id, file_url=file_url, tags=tag_names)
        mock_db_instance = Session()  # Создание реального экземпляра класса Session
        mock_get_db.return_value = mock_db_instance  # Использование реального экземпляра вместо мок-объекта
        mock_get_image_by_id.return_value = image

        result = await get_image(
            #user=mock_current_user,
            db=mock_db,
            image_id=image.id,
        )
        print (result)
        self.assertIsNotNone(result)
        self.assertEqual(description, result.description)
        self.assertIsInstance(result, Image)
        

    @patch("pyweb_team7_project.repository.images.get_image_by_id")
    @patch("pyweb_team7_project.database.db.get_db")
    async def test_get_image_with_invalid_id(self, mock_get_db, mock_get_image_by_id):
        mock_db = MagicMock(spec=Session)
        mock_current_user = MagicMock(spec=User)
        description = "Test description"
        user_id = 1
        image_id = None
        tag_names = ['tag1', 'tag2']
        file_url = 'https://example.com/image1.jpg'
        image = Image(id=image_id, description=description, user_id=user_id, file_url=file_url, tags=tag_names)
        mock_db_instance = Session()  # Создание реального экземпляра класса Session
        mock_get_db.return_value = mock_db_instance  # Использование реального экземпляра вместо мок-объекта
        mock_get_image_by_id.return_value = None

        try:
            result = await get_image(
            #user=mock_current_user,
            db=mock_db,
            image_id=image.id,
        )
            
            #self.fail("HTTPException not raised")
        except HTTPException as e:
            self.assertEqual(e.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(e.detail, "Image not found")


    @patch("pyweb_team7_project.repository.images.get_image_by_id")
    @patch("pyweb_team7_project.repository.images.delete_image")
    @patch("pyweb_team7_project.database.db.get_db")
    async def test_delete_image(self, mock_delete_image, mock_get_db, mock_get_image_by_id):
        mock_db = MagicMock(spec=Session)
        mock_current_user = MagicMock(spec=User)
        description = "Test description"
        user_id = 2
        image_id = 1
        tag_names = ['tag1', 'tag2']
        file_url = 'https://example.com/image1.jpg'
        image = Image(id=image_id, description=description, user_id=user_id, file_url=file_url, tags=tag_names)
        mock_db_instance = Session()  # Создание реального экземпляра класса Session
        mock_get_db.return_value = mock_db_instance
        mock_get_image_by_id.return_value = image
        user2 = User(id = 2, email = "test@example.com", username = "test", role =Role("admin"))
        result = await delete_image(
            image_id=image_id,
            current_user=user2,
            db=mock_db,
        )
        self.assertIsNotNone(result)

        # Проверка ошибки HTTPException при отсутствии разрешения
        user1 = User(id = 1, email = "test@example.com", username = "test", role =Role("moderator"))
        mock_current_user.id = 2
        mock_current_user.role = "user"
        with self.assertRaises(HTTPException) as exc_info:
            await delete_image(
                image_id=image_id,
                current_user=user1,
                db=mock_db,
            )
        self.assertEqual(exc_info.exception.status_code, status.HTTP_403_FORBIDDEN)

        # Проверка ошибки HTTPException при отсутствии изображения
        mock_get_image_by_id.return_value = None
        with self.assertRaises(HTTPException) as exc_info:
            await delete_image(
                image_id=image_id,
                current_user=user1,
                db=mock_db,
            )
        self.assertEqual(exc_info.exception.status_code, status.HTTP_404_NOT_FOUND)

    @patch("pyweb_team7_project.repository.images.get_image_by_id")
    @patch("pyweb_team7_project.repository.images.update_image_description")
    @patch("pyweb_team7_project.database.db.get_db")
    async def test_update_image(self, mock_get_db, mock_update_image_description, mock_get_image_by_id):
        mock_db = MagicMock(spec=Session)
        mock_current_user = MagicMock(spec=User)
        description = "Test description"
        new_description = "Test description created with new description"
        body =  UpdateImageModel
        body.new_description = new_description
        user_id = 2
        image_id = 1
        tag_names = ['tag1', 'tag2']
        file_url = 'https://example.com/image1.jpg'
        image = Image(id=image_id, description=description, user_id=user_id, file_url=file_url, tags=tag_names)
        mock_db_instance = Session()  # Создание реального экземпляра класса Session
        mock_get_db.return_value = mock_db_instance
        mock_get_image_by_id.return_value = image
        user2 = User(id = 2, email = "test@example.com", username = "test", role =Role("admin"))
        result = await update_image(
            image_id=image_id,
            current_user=user2,
            db=mock_db,
            body = body
        )
        self.assertIsNotNone(result)

        # Проверка ошибки HTTPException при отсутствии разрешения
        user1 = User(id = 1, email = "test@example.com", username = "test", role =Role("moderator"))
        mock_current_user.id = 2
        mock_current_user.role = "user"
        with self.assertRaises(HTTPException) as exc_info:
            await update_image(
                image_id=image_id,
                current_user=user1,
                db=mock_db,
                body = body
            )
        self.assertEqual(exc_info.exception.status_code, status.HTTP_403_FORBIDDEN)

        # Проверка ошибки HTTPException при отсутствии изображения
        mock_get_image_by_id.return_value = None
        with self.assertRaises(HTTPException) as exc_info:
            await update_image(
                image_id=image_id,
                current_user=user1,
                db=mock_db,
                body = body
            )
        self.assertEqual(exc_info.exception.status_code, status.HTTP_404_NOT_FOUND)

# class ImagesTestGetAll(unittest.IsolatedAsyncioTestCase):
#     @classmethod
#     def setUpClass(cls):
#         FastAPILimiter.init(app) 

#     @patch("pyweb_team7_project.database.db.get_db")
#     async def test_get_all_images(self, mock_get_db):
#         mock_response = [{"image_id": 1, "url": "example.com/image1.jpg"}, {"image_id": 2, "url": "example.com/image2.jpg"}]
#         mock_db = MagicMock(spec=Session)
#         with mock.patch("pyweb_team7_project.routes.images.get_all_images", return_value=mock_response):
#             response = await get_all_images(db=mock_db)
#             self.assertIsNotNone(response)
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(response.json, mock_response)
   
class TestTransformationsAutoColor(unittest.IsolatedAsyncioTestCase):

    @patch('pyweb_team7_project.routes.images.cloudinary.config')
    @patch('pyweb_team7_project.routes.images.cloudinary.CloudinaryImage.image')
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