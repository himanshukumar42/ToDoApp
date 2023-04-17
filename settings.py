from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

FLASK_APP = os.environ["FLASK_APP"]
FLASK_DEBUG = os.environ["FLASK_DEBUG"]
SECRET_KEY = os.environ["SECRET_KEY"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DATABASE_NAME}"
)