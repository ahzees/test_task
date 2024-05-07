import asyncio
import datetime
import os
from concurrent.futures import ThreadPoolExecutor

from conf import SAVE_DIR, images_logger
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from utils.file_processing import get_cached_file_path, process_uploaded_file

app = FastAPI()


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
