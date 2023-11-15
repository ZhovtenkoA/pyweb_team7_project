import os
import tempfile

import qrcode

from ..services.cloudinary import UploadService


async def get_qrcode_image_url(qr_data, folder_name):
    cloud_url = ""

    if qr_data:

        # Створюємо тимчасовий файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file_path = temp_file.name

        # Створюємо QR-код та зберігаємо зображення в тимчасовий файл
        img = qrcode.make(qr_data)
        img.save(temp_file_path)

        public_id = f"{folder_name}/{UploadService.generate_random_name(16)}"

        result = UploadService.upload(file=temp_file_path, public_id=public_id)

        if result:
            cloud_url = result.get('secure_url')

        # Видаляємо тимчасовий файл
        os.remove(temp_file_path)

    return cloud_url
