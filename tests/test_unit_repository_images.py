import unittest
from datetime import datetime, timedelta, date
from unittest.mock import MagicMock


from sqlalchemy.orm import Session

from pyweb_team7_project.database.models import User, Image
from pyweb_team7_project.schemas import CreateImageModel
from pyweb_team7_project.repository.images import (
    create_image_and_upload_to_cloudinary,
    get_image_by_id,
    update_image_description,
    delete_image

)


if __name__ == '__main__':
    unittest.main()

