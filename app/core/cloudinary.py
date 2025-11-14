import cloudinary
import cloudinary.uploader

from app.core.config import settings
from app.core.exceptions import ValidationException, FileUploadException

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    folder=settings.CLOUDINARY_FOLDER,
    secure=True
)

def upload_image(photo) -> dict:
    """Uploads an image to Cloudinary and returns the URL"""

    if photo.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise ValidationException(message="Image type not allowed")

    file_bytes = photo.file.read()

    if len(file_bytes) > settings.MAX_UPLOAD_SIZE:
        raise ValidationException(message="Image too large, max size 5MB")

    try:
        result = cloudinary.uploader.upload(
            file_bytes,
            resource_type="image",
            folder=settings.CLOUDINARY_FOLDER
        )
    except Exception as e:
        raise FileUploadException(message=str(e))

    return {
        "url": result.get("secure_url"),
        "public_id": result.get("public_id")
    }

def delete_image(url: str):
    """Deletes an image from Cloudinary and returns the URL"""
    cloudinary.uploader.destroy(url, resource_type="image")
