import os
import threading
import time
from typing import List

from conf import SAVE_DIR, redis_client
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from utils.image_processing import save_uploaded_files

app = FastAPI()


@app.post("/convert/")
async def convert_images(files: List[UploadFile] = File(...)):
    """
    Endpoint to handle image conversion.
    """
    # Create directory if it doesn't exist
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    start_time = time.time()  # Record start time

    # List to hold file paths for converted images
    converted_files = []

    # Process uploaded files
    for uploaded_file in files:
        # Check if grayscale image exists in cache
        cached_file = redis_client.get(f"gray_{uploaded_file.filename}")
        if cached_file:
            converted_files.append(cached_file.decode())
        else:
            # Save and convert images concurrently
            threading.Thread(
                target=save_uploaded_files, args=([uploaded_file],)
            ).start()

    # If only one file is converted, return it directly as FileResponse
    if len(converted_files) == 1:
        response = FileResponse(converted_files[0], media_type="image/jpeg")
    # If multiple files are converted, return a list of FileResponses
    else:
        response = [
            FileResponse(path, media_type="image/jpeg") for path in converted_files
        ]

    # Record end time
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

    return response
