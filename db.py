import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = os.getenv("DATABASE_URL")

URL = 'sqlite:///' + os.path.join(basedir, DATABASE_URL)

class Config:
    SQLALCHEMY_DATABASE_URI = URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False