import datetime
import os

from conf import images_logger, redis_client
from fastapi import HTTPException
from utils.image_processing import save_uploaded_files


def process_uploaded_file(uploaded_file):
    try:
        return save_uploaded_files(uploaded_file)
    except Exception as e:
        images_logger.error(f"Error processing file {uploaded_file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process the image")


def get_cached_file_path(uploaded_file):
    cached_file_path = redis_client.get(f"gray_{uploaded_file.filename}")
    if cached_file_path:
        cached_file_path = cached_file_path.decode()
        if os.path.exists(cached_file_path):
            images_logger.info(
                f"Returning cached image for {uploaded_file.filename};\
                time - {datetime.datetime.now()}"
            )
            return cached_file_path

    return None
