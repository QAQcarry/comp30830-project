import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # Database
    DB_USER     = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST     = os.environ.get("DB_HOST")
    DB_PORT     = os.environ.get("DB_PORT")
    DB_NAME     = os.environ.get("DB_NAME")

    # General
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    # Never hardcode secrets in production
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = False