import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '221'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'postgresql://booking_user:0001@localhost/booking_service_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False