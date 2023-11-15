import string
from random import choice

import cloudinary
import cloudinary.uploader

from pyweb_team7_project.conf.config import settings as config


class UploadService:
    cloudinary.config(
        cloud_name=config.cloudinary_name,
        api_key=config.cloudinary_api_key,
        api_secret=config.cloudinary_api_secret,
        secure=True
    )

    @staticmethod
    def generate_random_name(length=10):
        random_suffix = ''.join(choice(string.ascii_letters) for _ in range(length))
        return random_suffix

    @staticmethod
    def upload(file, public_id=None):
        if public_id:
            r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        else:
            r = cloudinary.uploader.upload(file)
        return r

