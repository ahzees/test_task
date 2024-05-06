import os

from conf import SAVE_DIR, images_logger, redis_client
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from utils.image_processing import save_uploaded_files

app = FastAPI()


@app.post("/convert/")
async def convert_images(uploaded_file: UploadFile = File(...)):
    """
    Endpoint to handle image conversion.
    """
    # Create directory if it doesn't exist
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Save and convert the image
    save_uploaded_files(uploaded_file)

    # Get the converted file path from Redis
    cached_file = redis_client.get(f"gray_{uploaded_file.filename}")
    if cached_file:
        converted_file_path = cached_file.decode()
    else:
        return {"error": "Failed to convert the image"}

    images_logger.info(f"Converted image - {converted_file_path}")
    # Return the converted image as a response
    return FileResponse(converted_file_path, media_type="image/jpeg")
