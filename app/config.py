import os
from hashlib import md5


class Configuration:
    encryptor = md5()

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_CONTAINER_NAME')}:5432/{os.getenv('POSTGRES_DB')}"
    SECRET_KEY = encryptor.digest()
