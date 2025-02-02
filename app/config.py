from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DB_HOST = os.getenv('HOST_DB', "localhost")
    DB_USER = os.getenv('USER_DB', "root")
    DB_PASSWORD = os.getenv('PASS_DB', "")
    DB_DATABSE = os.getenv('DB')
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABSE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
    DEBUG = True