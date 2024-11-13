from PIL import Image
from fastapi import UploadFile

from app.core.config import settings

def validate_uploaded_image(file: UploadFile) -> str | None:
    """ Validate file name, type, size, image format, image dimensions.
    """

    if not file.filename:
        return 'Invalid file name'

    if not file.content_type or not file.content_type.startswith('image/'):
        return 'Invalid file type'

    if not file.size or file.size > settings.USER_MAX_UPLOAD_SIZE:
        return f'File size is too large (maximum {settings.USER_MAX_UPLOAD_SIZE} bytes)'

    try:
        image = Image.open(file.file)
        image.verify()
    except Exception as e:
        return f'Invalid image file: {e}'

    if image.width < settings.USER_IMAGE_MIN_WIDTH or image.height < settings.USER_IMAGE_MIN_HEIGHT:
        return 'Image dimensions are too small (minimum {settings.USER_IMAGE_MIN_WIDTH}x{settings.USER_IMAGE_MIN_HEIGHT})'

    if image.width > settings.USER_IMAGE_MAX_WIDTH or image.height > settings.USER_IMAGE_MAX_HEIGHT:
        return f'Image dimensions are too large (maximum {settings.USER_IMAGE_MAX_WIDTH}x{settings.USER_IMAGE_MAX_HEIGHT})'

    return None
