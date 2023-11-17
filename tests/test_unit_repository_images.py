import unittest
import cloudinary

from unittest.mock import MagicMock, Mock

from sqlalchemy.orm import Session

from pyweb_team7_project.database.models import User, Image, Tag
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
        print(result, existing_image)
        self.assertEqual(result, existing_image)


if __name__ == '__main__':
    unittest.main()

