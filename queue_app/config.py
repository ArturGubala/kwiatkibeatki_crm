from hashlib import md5


class Configuration:
    encryptor = md5()

    DEBUG = True
    SECRET_KEY = encryptor.digest()
