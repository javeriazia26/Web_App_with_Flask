import os

from dotenv import load_dotenv

print("Current directory:", os.getcwd())
print("Config file:", __file__)

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


    print("SECRET_KEY:", os.getenv("SECRET_KEY"))
    print("DATABASE_URL:", os.getenv("DATABASE_URL"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
