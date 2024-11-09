# import secrets
# secret_key = secrets.token_hex(32)
# print(secret_key)

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY','1cf0a6e69b27be8126adbcc37bfea2a8e861dff303018f48bf5abd2c249866fc')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False