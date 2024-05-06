import os

import cv2
from conf import SAVE_DIR, redis_client
from fastapi import UploadFile


def convert_to_gray(input_path: str, output_path: str) -> str:
    image = cv2.imread(input_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, gray_image)


def save_uploaded_files(uploaded_file: UploadFile):
    """
    Function to save uploaded files to the specified directory.
    """
    file_content = uploaded_file.file.read()
    file_path = os.path.join(SAVE_DIR, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    # Convert and save grayscale image
    gray_file_path = os.path.join(SAVE_DIR, f"gray_{uploaded_file.filename}")
    convert_to_gray(file_path, gray_file_path)
    # Cache the grayscale image
    redis_client.set(f"gray_{uploaded_file.filename}", gray_file_path)
