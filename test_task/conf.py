import logging
import os

import dotenv
import redis

images_logger = logging.getLogger(__name__)
images_logger.setLevel(logging.INFO)
images_logger.addHandler(logging.FileHandler("images_logger.log"))

dotenv.load_dotenv()


host = os.environ["HOST"]
port = os.environ["PORT"]
password = os.environ["PASSWORD"]

SAVE_DIR = "images"


redis_client = redis.Redis(host=host, port=port, password=password)
