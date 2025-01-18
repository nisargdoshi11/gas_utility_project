# utils/helpers.py

import os
from django.conf import settings

# Check if the uploaded file is of an allowed type (e.g., images, PDFs, etc.)
ALLOWED_FILE_TYPES = ['application/pdf', 'image/jpeg', 'image/png']

def is_allowed_file(file):
    """
    Helper function to check if the uploaded file is of an allowed type.
    """
    return file.content_type in ALLOWED_FILE_TYPES

def get_file_extension(file):
    """
    Helper function to get the file extension from the file name.
    """
    return os.path.splitext(file.name)[1].lower()

def save_uploaded_file(file, path=settings.MEDIA_ROOT):
    """
    Helper function to save the uploaded file in a specified directory.
    """
    file_path = os.path.join(path, file.name)
    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return file_path
