import unittest
from unittest.mock import patch, MagicMock
import io
import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pyweb_team7_project.routes import images
from pyweb_team7_project.database.models import User, Image
from pyweb_team7_project.repository.images import create_image_and_upload_to_cloudinary, get_image_by_id, get_all_images, delete_image
from pyweb_team7_project.schemas import ImageResponse
from pyweb_team7_project.conf.config import settings


class ImagesTest(unittest.TestCase):
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
        tags = "tag1, tag2"
        test_image_path = os.path.join(
            os.path.dirname(__file__), "test_images", "test.jpg"
        )
        with open(test_image_path, "rb") as f:
            file_data = f.read()
        file = UploadFile(filename="test.jpg", file=io.BytesIO(file_data))

        result = await images.create_image(
            description=description,
            tags=tags,
            file=file,
            current_user=mock_current_user,
            db=mock_db,
        )

        mock_repository_images.create_image_and_upload_to_cloudinary.assert_called_once_with(
            mock_db,
            file,
            description=description,
            user_id=mock_current_user.id,
            tag_names=["tag1", "tag2"],
        )
        self.assertEqual(result, mock_response)

    @patch("pyweb_team7_project.repository.images")
    @patch("pyweb_team7_project.services.auth.auth_service")
    @patch("pyweb_team7_project.database.db.get_db")
    async def test_create_image_with_invalid_data(
        self, mock_get_db, mock_auth_service, mock_repository_images
    ):
        # Test case with invalid data
        mock_db = MagicMock(spec=Session)
        mock_current_user = MagicMock(spec=User)
        mock_file = MagicMock(spec=UploadFile)

        mock_get_db.return_value = mock_db
        mock_auth_service.get_current_user.return_value = mock_current_user

        description = ""  # Empty description
        tags = "tag1, tag2"
        file = None  # Invalid file

        result = await images.create_image(
            description=description,
            tags=tags,
            file=file,
            current_user=mock_current_user,
            db=mock_db,
        )

        mock_repository_images.create_image_and_upload_to_cloudinary.assert_not_called()
        self.assertIsNone(result)

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

        mock_get_db.return_value = mock_db
        mock_auth_service.get_current_user.return_value = mock_current_user
        mock_repository_images.create_image_and_upload_to_cloudinary.return_value = mock_response

        description = "A" * 1000  # Maximum length description
        tags = "tag1, " + "tag2," * 1000  # Maximum number of tags

        result = await images.create_image(
            description=description,
            tags=tags,
            file=mock_file,
            current_user=mock_current_user,
            db=mock_db,
        )

        mock_repository_images.create_image_and_upload_to_cloudinary.assert_called_once_with(
            mock_db,
            mock_file,
            description=description,
            user_id=mock_current_user.id,
            tag_names=["tag1"] + ["tag2"] * 999,
        )
        self.assertEqual(result, mock_response)

    @patch("pyweb_team7_project.repository.images.get_image_by_id")
    async def test_get_image_with_valid_id(self, mock_get_image_by_id):
        mock_db = MagicMock(spec=Session)
        mock_current_user = MagicMock(spec=User)
        image_id = 1
        mock_image = MagicMock(spec=ImageResponse)
        mock_get_image_by_id.return_value = mock_image

        result = get_image_by_id(
            image_id=image_id,
            user=mock_current_user,
            db=mock_db,
        )

        mock_get_image_by_id.assert_called_once_with(
            mock_current_user, mock_db, image_id
        )
        self.assertEqual(result, mock_image)

    @patch("pyweb_team7_project.repository.images.get_image_by_id")
    async def test_get_image_with_invalid_id(self, mock_get_image_by_id):
        mock_db = MagicMock(spec=Session)
        mock_current_user = MagicMock(spec=User)
        image_id = None
        mock_get_image_by_id.return_value = None

        try:
            get_image_by_id(
                image_id=image_id,
                user=mock_current_user,
                db=mock_db,
            )
            
            self.fail("HTTPException not raised")
        except HTTPException as e:
            self.assertEqual(e.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(e.detail, "Image not found")

        mock_get_image_by_id.assert_called_once_with(
            mock_current_user, mock_db, image_id
        )

    @patch("pyweb_team7_project.repository.images.get_image_by_idd")
    @patch("pyweb_team7_project.repository.images.delete_image")
    async def test_delete_image_with_valid_id(self, mock_delete_image, mock_get_image_by_id):
        mock_db = MagicMock()
        mock_current_user = MagicMock()
        image_id = 1
        mock_image = MagicMock()
        mock_get_image_by_id.return_value = mock_image

        result = await delete_image(
            image_id=image_id,
            current_user=mock_current_user,
            db=mock_db,
        )

        mock_get_image_by_id.assert_called_once_with(
            user=mock_current_user, image_id=image_id, db=mock_db
        )
        mock_delete_image.assert_called_once_with(
            current_user=mock_current_user, db=mock_db, image_id=image_id
        )
        self.assertEqual(result, mock_image)

    @patch("pyweb_team7_project.api.routes.images.repository_images.get_image_by_id")
    async def test_delete_image_with_invalid_id(self, mock_get_image_by_id):
        mock_db = MagicMock()
        mock_current_user = MagicMock()
        image_id = None
        mock_get_image_by_id.return_value = None

        try:
            await delete_image(
                image_id=image_id,
                current_user=mock_current_user,
                db=mock_db,
            )
            self.fail("HTTPException not raised")
        except HTTPException as e:
            self.assertEqual(e.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(e.detail, "Image not found")

        mock_get_image_by_id.assert_called_once_with(
            user=mock_current_user, image_id=image_id, db=mock_db
        )
    @patch("pyweb_team7_project.api.routes.images.cloudinary")
    async def test_transformations_grayscale(self, mock_cloudinary):
        mock_db = MagicMock()
        mock_current_user = MagicMock()
        image_id = 1
        mock_image = MagicMock()
        mock_image.public_id = "public_id"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_image

        transformed_url = "transformed_url"
        mock_cloudinary.CloudinaryImage.return_value.image.return_value = transformed_url

        result = await images.transformations_grayscale(
            image_id=image_id,
            current_user=mock_current_user,
            db=mock_db,
        )

        mock_db.query.assert_called_once_with(Image)
        mock_db.query.return_value.filter.assert_called_once_with(
            and_(Image.id == image_id, Image.user_id == mock_current_user.id)
        )
        mock_db.query.return_value.filter.return_value.first.assert_called_once()
        mock_cloudinary.config.assert_called_once_with(
            cloud_name=settings.cloudinary_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )
        mock_cloudinary.CloudinaryImage.assert_called_once_with(mock_image.public_id)
        mock_cloudinary.CloudinaryImage.return_value.image.assert_called_once_with(
            effect="grayscale"
        )
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_image)
        self.assertEqual(result, mock_image)
    @patch("pyweb_team7_project.api.routes.images.cloudinary")
    async def test_transformations_auto_color(self, mock_cloudinary):
        mock_db = MagicMock()
        mock_current_user = MagicMock()
        image_id = 1
        mock_image = MagicMock()
        mock_image.public_id = "public_id"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_image

        transformed_url = "transformed_url"
        mock_cloudinary.CloudinaryImage.return_value.image.return_value = transformed_url

        result = await images.transformations_auto_color(
            image_id=image_id,
            current_user=mock_current_user,
            db=mock_db,
        )

        mock_db.query.assert_called_once_with(Image)
        mock_db.query.return_value.filter.assert_called_once_with(
            and_(Image.id == image_id, Image.user_id == mock_current_user.id)
        )
        mock_db.query.return_value.filter.return_value.first.assert_called_once()
        mock_cloudinary.config.assert_called_once_with(
            cloud_name=settings.cloudinary_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )
        mock_cloudinary.CloudinaryImage.assert_called_once_with(mock_image.public_id)
        mock_cloudinary.CloudinaryImage.return_value.image.assert_called_once_with(
            effect="auto_color"
        )
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_image)
        self.assertEqual(result, mock_image)
    @patch("pyweb_team7_project.api.routes.images.cloudinary")
    async def test_transformations_sepia(self, mock_cloudinary):
        mock_db = MagicMock()
        mock_current_user = MagicMock()
        image_id = 1
        mock_image = MagicMock()
        mock_image.public_id = "public_id"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_image

        transformed_url = "transformed_url"
        mock_cloudinary.CloudinaryImage.return_value.image.return_value = transformed_url

        result = await images.transformations_sepia(
            image_id=image_id,
            current_user=mock_current_user,
            db=mock_db,
        )

        mock_db.query.assert_called_once_with(Image)
        mock_db.query.return_value.filter.assert_called_once_with(
            and_(Image.id == image_id, Image.user_id == mock_current_user.id)
        )
        mock_db.query.return_value.filter.return_value.first.assert_called_once()
        mock_cloudinary.config.assert_called_once_with(
            cloud_name=settings.cloudinary_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )
        mock_cloudinary.CloudinaryImage.assert_called_once_with(mock_image.public_id)
        mock_cloudinary.CloudinaryImage.return_value.image.assert_called_once_with(
            effect="sepia"
        )
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_image)
        self.assertEqual(result, mock_image)

if __name__ == "__main__":
    unittest.main()