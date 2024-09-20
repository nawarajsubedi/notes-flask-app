import os


class Config:
    SECRET_KEY = "d$u1A2sB@e4f5G#hI7jK*L8mN9oP0qR1sT2uV3wX4yZ!aB@cD#eF^gH&*iJkL(MnO)pQ"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost/notes_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = "redis://127.0.0.1/0"
