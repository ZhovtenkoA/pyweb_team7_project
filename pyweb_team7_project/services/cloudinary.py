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
        """
        The generate_random_name function generates a random string of length 10.
            Args:
                length (int): The number of characters in the generated string. Defaults to 10.

        :param length: Set the length of the random string that is generated
        :return: A string of random letters
        """
        random_suffix = ''.join(choice(string.ascii_letters) for _ in range(length))
        return random_suffix

    @staticmethod
    def upload(file, public_id=None):
        """
        The upload function takes a file and an optional public_id.
        If the public_id is provided, it will overwrite any existing image with that id.
        Otherwise, it will upload the image to Cloudinary and return a dictionary containing information about the uploaded file.

        :param file: Specify the file to upload
        :param public_id: Set the public id of the image
        :return: A dictionary
        """
        if public_id:
            r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        else:
            r = cloudinary.uploader.upload(file)
        return r

