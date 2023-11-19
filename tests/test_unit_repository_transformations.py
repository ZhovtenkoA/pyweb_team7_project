import unittest
from unittest.mock import MagicMock, patch
import asyncio

from sqlalchemy.orm import Session

from pyweb_team7_project.database.models import Image
from pyweb_team7_project.repository.transformations import transformations_grayscale, transformations_auto_color, transformations_sepia, transformations_blur, transformations_brown_outline

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

class TestTransformationsBrownOutline(unittest.TestCase):

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

if __name__ == '__main__':
    asyncio.run(unittest.main())