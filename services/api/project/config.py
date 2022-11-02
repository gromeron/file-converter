import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "secret-phrase"
    #JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    #JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)