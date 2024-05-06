import os

import dotenv
import redis

dotenv.load_dotenv()


host = os.environ["HOST"]
port = os.environ["PORT"]
password = os.environ["PASSWORD"]

SAVE_DIR = "images"


redis_client = redis.Redis(host=host, port=port, password=password)
