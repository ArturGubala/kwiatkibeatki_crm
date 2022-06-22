import os
from dotenv import load_dotenv
from hashlib import md5

load_dotenv()


class Configuration:
    encryptor = md5()

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = encryptor.digest()
