#!/usr/bin/python3
import os


class Config:
    """
    base configuration class
    """
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_HEADER_TYPE = 'Bearer'

    DEBUG = False
    TESTING = False
    ENV = 'production'

class DevelopmentConfig(Config):
    """
    dvpt env config
    """
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    """
    testing env config
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """
    production env config
    """
    DEBUG = False
    ENV = 'production'