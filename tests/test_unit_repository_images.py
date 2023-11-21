import unittest
from unittest.mock import MagicMock
import asyncio
from sqlalchemy.orm import Session

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

from unittest.mock import patch

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

    

    # async def test_create_image_and_upload_to_cloudinary(self):
    #     # Mock the necessary objects and methods
    #     file_data = b"dummy_file_data"
    #     mock_file = io.BytesIO(file_data)

    #     # Create a temporary file
    #     temp_file_path = tempfile.mktemp(suffix=".jpg")
    #     with open(temp_file_path, "wb") as temp_file:
    #         temp_file.write(mock_file.getvalue())

    #     cloudinary_upload_result = {
    #         "secure_url": "https://example.com/image.jpg",
    #         "public_id": "public_id",
    #     }
        
    #     with patch("pyweb_team7_project.repository.images.create_image_and_upload_to_cloudinary") as mock_upload:
    #         mock_upload.return_value = cloudinary_upload_result

    #         # Call the function
    #         temp_file_wrapper = TemporaryFileWrapper(temp_file_path)
    #         image = await create_image_and_upload_to_cloudinary(
    #             db=self.session,
    #             user_id=self.user.id,
    #             file=temp_file_wrapper,  # Use the file attribute of the wrapper
    #             description=self.description,
    #             tag_names=self.tag_names
    #         )

    #     # Assertions
    #     self.assertIsInstance(image, Image)
    #     self.assertEqual(image.file_url, cloudinary_upload_result["secure_url"])
    #     self.assertEqual(image.public_id, cloudinary_upload_result["public_id"])
    #     self.assertEqual(image.description, self.description)
    #     self.assertEqual(image.user_id, self.user.id)
    #     self.assertEqual(len(image.tags), len(self.tag_names))
    #     self.assertTrue(all(tag.name in self.tag_names for tag in image.tags))


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
