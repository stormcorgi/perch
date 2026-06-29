"""
    for describe app config, especially LIB paths (video & book libraries)
"""

import os

# ── paths ──────────────────────────────────────────────
PROD_DB  = os.path.join(os.getcwd(), "instance", "perch.sqlite")
PROD_VIDEO_LIB = os.path.join(os.getcwd(), "perch", "static", "eagle_library")
PROD_BOOK_LIB  = os.path.join(os.getcwd(), "perch", "static", "eagle_book_library")

DEV_DB   = os.path.join(os.getcwd(), "tests", "perch.sqlite")
DEV_VIDEO_LIB = os.path.join(os.getcwd(), "tests", "sample.library")
DEV_BOOK_LIB  = os.path.join(os.getcwd(), "tests", "sample_book.library")  # 後で作るかも


class Development(object):
    DEBUG = True
    DATABASE = DEV_DB
    LIB_PATH_VIDEO = DEV_VIDEO_LIB
    LIB_PATH_BOOK  = DEV_BOOK_LIB
    LIB_PATH = DEV_VIDEO_LIB  # backward compat for existing code referencing LIB_PATH directly


class Testing(object):
    DEBUG = True
    DATABASE = DEV_DB
    LIB_PATH_VIDEO = DEV_VIDEO_LIB
    LIB_PATH_BOOK  = DEV_BOOK_LIB
    LIB_PATH = DEV_VIDEO_LIB  # backward compat


class Production(object):
    DEBUG = False
    DATABASE = PROD_DB
    LIB_PATH_VIDEO = PROD_VIDEO_LIB
    LIB_PATH_BOOK  = PROD_BOOK_LIB
    LIB_PATH = PROD_VIDEO_LIB  # backward compat
