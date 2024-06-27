import datetime


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://user_manager:0001@localhost:5432/user_service_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '221'
    JWT_SECRET_KEY = '3331'
    PORT = 5001
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    EMAIL_SERVICE_URL = "http://localhost:5002/email/send"