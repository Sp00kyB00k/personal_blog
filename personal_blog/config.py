import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLACLHEMY_DATABASE_URI') or \
        'sqlite:///test.db'
