import unittest
from unittest.mock import patch
from pyweb_team7_project.services.qrcode_generation import get_qrcode_image_url
import asyncio


class TestGetQRCodeImageUrl(unittest.TestCase):
    @patch("tempfile.NamedTemporaryFile")
    @patch("qrcode.make")
    @patch("pyweb_team7_project.services.cloudinary.UploadService.generate_random_name")
    @patch("pyweb_team7_project.services.cloudinary.UploadService.upload")
    @patch("os.remove")
    async def test_get_qrcode_image_url_with_data(
        self,
        mock_remove,
        mock_upload,
        mock_generate_random_name,
        mock_make,
        mock_tempfile,
    ):
        # Mock the necessary objects and methods
        qr_data = "test_data"
        folder_name = "test_folder"
        temp_file_path = "test_temp_file.png"
        cloud_url = "https://example.com/test_url.png"

        # Configure the mock objects
        mock_tempfile.return_value.__enter__.return_value.name = temp_file_path
        mock_make.return_value.save.return_value = None
        mock_generate_random_name.return_value = "test_name"
        mock_upload.return_value = {"secure_url": cloud_url}

        # Call the function being tested
        result = await get_qrcode_image_url(qr_data, folder_name)

        # Assertions
        self.assertEqual(result, cloud_url)
        mock_tempfile.assert_called_once_with(delete=False, suffix=".png")
        mock_make.assert_called_once_with(qr_data)
        mock_make.return_value.save.assert_called_once_with(temp_file_path)
        mock_generate_random_name.assert_called_once_with(16)
        mock_upload.assert_called_once_with(
            file=temp_file_path, public_id=f"{folder_name}/test_name"
        )
        mock_remove.assert_called_once_with(temp_file_path)

    async def test_get_qrcode_image_url_with_no_data(self):
        # Mock the necessary objects and methods
        qr_data = None
        folder_name = "test_folder"

        # Call the function being tested
        result = await get_qrcode_image_url(qr_data, folder_name)

        # Assertions
        self.assertEqual(result, "")

    @patch("tempfile.NamedTemporaryFile")
    @patch("qrcode.make")
    @patch("pyweb_team7_project.services.cloudinary.UploadService.generate_random_name")
    @patch("pyweb_team7_project.services.cloudinary.UploadService.upload")
    @patch("os.remove")
    async def test_get_qrcode_image_url_with_exception(
        self,
        mock_remove,
        mock_upload,
        mock_generate_random_name,
        mock_make,
        mock_tempfile,
    ):
        # Mock the necessary objects and methods
        qr_data = "test_data"
        folder_name = "test_folder"
        temp_file_path = "test_temp_file.png"

        # Configure the mock objects
        mock_tempfile.return_value.__enter__.return_value.name = temp_file_path
        mock_make.side_effect = Exception("Mocked exception")

        # Call the function being tested
        result = await get_qrcode_image_url(qr_data, folder_name)

        # Assertions
        self.assertEqual(result, "")
        mock_tempfile.assert_called_once_with(delete=False, suffix=".png")
        mock_make.assert_called_once_with(qr_data)
        mock_remove.assert_called_once_with(temp_file_path)

    @patch("tempfile.NamedTemporaryFile")
    @patch("qrcode.make")
    @patch("pyweb_team7_project.services.cloudinary.UploadService.generate_random_name")
    @patch("pyweb_team7_project.services.cloudinary.UploadService.upload")
    @patch("os.remove")
    async def test_get_qrcode_image_url_with_no_temp_file(
        self,
        mock_remove,
        mock_upload,
        mock_generate_random_name,
        mock_make,
        mock_tempfile,
    ):
        # Mock the necessary objects and methods
        qr_data = "test_data"
        folder_name = "test_folder"
        cloud_url = "https://example.com/test_url.png"

        # Configure the mock objects
        mock_tempfile.return_value.__enter__.side_effect = OSError("Mocked OSError")
        mock_make.return_value.save.return_value = None
        mock_generate_random_name.return_value = "test_name"
        mock_upload.return_value = {"secure_url": cloud_url}

        # Call the function being tested
        result = await get_qrcode_image_url(qr_data, folder_name)

        # Assertions
        self.assertEqual(result, cloud_url)
        mock_tempfile.assert_called_once_with(delete=False, suffix=".png")
        mock_make.assert_called_once_with(qr_data)


class TestGetQRCodeImageUrl(unittest.TestCase):
    @patch("tempfile.NamedTemporaryFile")
    @patch("qrcode.make")
    @patch("pyweb_team7_project.services.cloudinary.UploadService.generate_random_name")
    @patch("pyweb_team7_project.services.cloudinary.UploadService.upload")
    @patch("os.remove")
    def test_get_qrcode_image_url_with_data(
        self,
        mock_remove,
        mock_upload,
        mock_generate_random_name,
        mock_make,
        mock_tempfile,
    ):
        # Mock the necessary objects and methods
        qr_data = "test_data"
        folder_name = "test_folder"
        temp_file_path = "test_temp_file.png"
        cloud_url = "https://example.com/test_url.png"

        # Configure the mock objects
        mock_tempfile.return_value.__enter__.return_value.name = temp_file_path
        mock_make.return_value.save.return_value = None
        mock_generate_random_name.return_value = "test_name"
        mock_upload.return_value = {"secure_url": cloud_url}

        # Call the function being tested
        result = asyncio.run(get_qrcode_image_url(qr_data, folder_name))

        # Assertions
        self.assertEqual(result, cloud_url)
        mock_tempfile.assert_called_once_with(delete=False, suffix=".png")
        mock_make.assert_called_once_with(qr_data)
        mock_make.return_value.save.assert_called_once_with(temp_file_path)
        mock_generate_random_name.assert_called_once_with(16)
        mock_upload.assert_called_once_with(
            file=temp_file_path, public_id=f"{folder_name}/test_name"
        )
        mock_remove.assert_called_once_with(temp_file_path)

    def test_get_qrcode_image_url_with_no_data(self):
        # Mock the necessary objects and methods
        qr_data = None
        folder_name = "test_folder"

        # Call the function being tested
        result = asyncio.run(get_qrcode_image_url(qr_data, folder_name))

        # Assertions
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
