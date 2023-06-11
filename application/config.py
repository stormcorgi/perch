import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration"""


class ProductionConfig(Config):
    """Production configuration"""

    config = configparser.ConfigParser()
    config.read(os.path.join(basedir, "../config.ini"))
    LIB_PATH = config["DEFAULT"]["EagleLibPath"]


class DevelopmentConfig(Config):
    """Development configuration"""

    config = configparser.ConfigParser()
    config.read(os.path.join(basedir, "../config.ini"))
    LIB_PATH = config["DEFAULT"]["EagleLibPath"]


class TestingConfig(Config):
    """Testing configuration"""

    config = configparser.ConfigParser()
    config.read(os.path.join(basedir, "../config.ini"))
    LIB_PATH = config["DEFAULT"]["EagleLibPath"]
    TESTING = True
