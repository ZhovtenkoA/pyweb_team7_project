import unittest
import cloudinary

from unittest.mock import MagicMock


from sqlalchemy.orm import Session

from pyweb_team7_project.database.models import User, Image
from pyweb_team7_project.conf.config import settings
from pyweb_team7_project.repository.images import (
    create_image_and_upload_to_cloudinary,
    get_image_by_id,
    update_image_description,
    delete_image
)


class TestImageFunctions(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_create_image_and_upload_to_cloudinary(self):

        file = MagicMock()
        file.file = "dummy_file_content"
        description = "Test Image"
        user_id = 1
        tag_names = ["tag1", "tag2"]

        image = await create_image_and_upload_to_cloudinary(
            db=self.session, file=file, description=description, user_id=user_id, tag_names=tag_names
        )

        self.assertIsInstance(image, Image)
        self.assertEqual(image.description, description)
        self.assertEqual(image.user_id, user_id)
        self.assertEqual(len(image.tags), len(tag_names))

    async def test_get_image_by_id(self):
        image_id = 1
        image = Image(id=image_id, user_id=self.user.id)
        self.session.query().filter().first.return_value = image

        result = await get_image_by_id(user=self.user, db=self.session, image_id=image_id)

        self.assertEqual(result, image)

    async def test_update_image_description(self):
        image_id = 1
        new_description = "Updated Description"
        existing_image = Image(id=image_id, user_id=self.user.id, description="Old Description")
        self.session.query().filter().first.return_value = existing_image

        result = await update_image_description(
            user=self.user, db=self.session, image_id=image_id, new_description=new_description
        )

        self.assertEqual(result.description, new_description)

    async def test_delete_image(self):
        image_id = 1
        existing_image = Image(id=image_id, user_id=self.user.id)
        self.session.query().filter().first.return_value = existing_image

        result = await delete_image(user=self.user, db=self.session, image_id=image_id)

        self.assertEqual(result, existing_image)


def sign_request(params, options):
    api_key = options.get("api_key", cloudinary.config().api_key)
    if not api_key:
        raise ValueError("Must supply api_key")

if __name__ == '__main__':
    unittest.main()

