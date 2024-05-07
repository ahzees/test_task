import asyncio
import datetime
import os
from concurrent.futures import ThreadPoolExecutor

from conf import SAVE_DIR, images_logger, redis_client
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from utils.image_processing import save_uploaded_files

app = FastAPI()


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


@app.post("/convert/")
async def convert_images(uploaded_file: UploadFile = File(...)):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    cached_file_path = None
    with ThreadPoolExecutor() as executor:
        cached_file_path = executor.submit(get_cached_file_path, uploaded_file).result()

    if cached_file_path:
        return FileResponse(cached_file_path, media_type="image/jpeg")

    loop = asyncio.get_event_loop()
    gray_file_path = await loop.run_in_executor(
        None, process_uploaded_file, uploaded_file
    )

    images_logger.info(
        f"Converted image - {gray_file_path}; time - {datetime.datetime.now()}"
    )
    return FileResponse(
        gray_file_path,
        media_type="image/jpeg"
        if uploaded_file.content_type.startswith("image/jpeg")
        else "image/png",
    )
