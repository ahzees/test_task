import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

import pytest
import requests
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(
    os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "test_task"
    )
)

from test_task.main import app

client = TestClient(app)

SAVE_DIR = os.path.join(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "tests/test_images"
)
NUM_IMAGES = 15


def download_image(image_url, image_path):
    response = requests.get(image_url)
    with open(image_path, "wb") as f:
        f.write(response.content)


@pytest.fixture(scope="session")
def create_test_images():
    # Створюємо тестову папку для зберігання зображень, якщо її не існує
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Створюємо пул потоків для завантаження зображень
    with ThreadPoolExecutor(max_workers=NUM_IMAGES) as executor:
        # Завантажуємо тестові зображення з веб-сайту "https://picsum.photos/"
        futures = []
        for i in range(NUM_IMAGES):
            image_url = f"https://picsum.photos/200/300?random={i}"
            image_path = os.path.join(SAVE_DIR, f"test_image_{i}.jpg")
            futures.append(executor.submit(download_image, image_url, image_path))

        # Очікуємо завершення всіх потоків
        for future in futures:
            future.result()

    yield


def test_upload_image(create_test_images):
    files = []
    for i in range(NUM_IMAGES):
        files.append(
            (
                "uploaded_file",
                (
                    f"test_image_{i}.jpg",
                    open(os.path.join(SAVE_DIR, f"test_image_{i}.jpg"), "rb"),
                    "image/jpeg",
                ),
            )
        )

    response = client.post("/convert/", files=files)
    assert (
        response.status_code == 200
    ), f"Помилка при виконанні запиту: {response.status_code}"


def test_conversion_accuracy(create_test_images):
    files = []
    for i in range(NUM_IMAGES):
        files.append(
            (
                "uploaded_file",
                (
                    f"test_image_{i}.jpg",
                    open(os.path.join(SAVE_DIR, f"test_image_{i}.jpg"), "rb"),
                    "image/jpeg",
                ),
            )
        )

    response = client.post("/convert/", files=files)
    assert (
        response.status_code == 200
    ), f"Помилка при виконанні запиту: {response.status_code}"
    assert (
        response.headers["Content-Type"] == "image/jpeg"
    ), "Неправильний тип вмісту відповіді"


def test_concurrent_requests(create_test_images):
    urls = ["/convert/"] * NUM_IMAGES
    responses = []

    with ThreadPoolExecutor(max_workers=NUM_IMAGES) as executor:
        futures = []
        for i, url in enumerate(urls):
            image_path = os.path.join(SAVE_DIR, f"test_image_{i}.jpg")
            futures.append(
                executor.submit(
                    requests.post,
                    f"http://localhost:8000{url}",
                    files={
                        "uploaded_file": (
                            os.path.basename(image_path),
                            open(image_path, "rb"),
                            "image/jpeg",
                        )
                    },
                )
            )

        for future in futures:
            response = future.result()
            responses.append(response)

    for response in responses:
        assert (
            response.status_code == 200
        ), f"Помилка при виконанні запиту: {response.status_code}"
    delete_files_except_current_file(os.path.dirname(__file__))


def delete_files_except_current_file(directory):
    for filename in os.listdir(directory):
        if filename != os.path.basename(__file__):
            filepath = os.path.join(directory, filename)
            try:
                if os.path.isfile(filepath):
                    os.remove(filepath)
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath)
            except Exception as e:
                print(f"Failed to delete {filepath}: {e}")
