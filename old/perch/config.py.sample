"""
    for describe app config, especially PROD_LIB for eagle library path
"""

import os
PROD_LIB = os.path.join(os.getcwd(), "perch/static/eagle_library")
PROD_DB = os.path.join(os.getcwd(), "instance/perch.sqlite")

DEV_LIB = os.path.join(os.getcwd(), "tests/sample.library")
DEV_DB = os.path.join(os.getcwd(), "tests/perch.sqlite")


class Development(object):
    """
    for dev configuration
    use DEV-DB, DEV-PATH
    """
    DEBUG = True
    DATABASE = DEV_DB
    LIB_PATH = DEV_LIB


class Testing(object):
    """
    for test configuration
    use DEV-DB, DEV-PATH
    """
    DEBUG = True
    # LIB_PATH = PROD_LIB
    LIB_PATH = DEV_LIB
    DATABASE = DEV_DB


class Production(object):
    """
    for production configuration
    use real DB, LIB
    """
    DEBUG = False
    DATABASE = PROD_DB
    LIB_PATH = PROD_LIB
