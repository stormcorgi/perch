"""import pytest, sqlalchemy, app.perchdb, tests.conftest for CONST"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database
from app.perchdb import Base, Actress, Movie, Tag
from app.perchdb import update_actress, update_files
from tests.conftest import SAMPLE_LIB, SAMPLE_DB_PATH


@pytest.fixture(name="db_session")
def fixture_db():
    """generate test DB(when test finished,DB file will be erased)"""
    test_engine = create_engine(SAMPLE_DB_PATH)
    test_session = sessionmaker(test_engine)

    # create DB tables inherited Base
    Base.metadata.create_all(test_engine)
    # return Session(), and wait test case finish
    yield test_session()

    # remove db file
    drop_database(SAMPLE_DB_PATH)


def test_update_actress(db_session):
    """parse master metadata.json, update DB actress table"""
    update_actress(db_session, SAMPLE_LIB, True)


def test_update_files(db_session):
    """parse each file's metadata.json, update DB file,tag table"""
    update_files(db_session, SAMPLE_LIB, True)

# actress


def test_actress_all(db_session):
    """update_actress, then verify all data query-able"""
    update_actress(db_session, SAMPLE_LIB, True)
    all_actresses = Actress.all(db_session)
    for actress in all_actresses:
        assert isinstance(actress.id, int) is True
        assert isinstance(actress.actressid, str) is True
        assert isinstance(actress.name, str) is True


def test_actress_get_by_name(db_session):
    """update_actress, then query by name string"""
    update_actress(db_session, SAMPLE_LIB, True)
    record = Actress.get_by_name("food", db_session)
    assert record is not None
    assert record.id == 3
    assert record.actressid == "L03BHCN6FV119"
    assert record.name == "food"
    record = Actress.get_by_name("non-exist-name", db_session)
    assert record is None

# movie


def test_movie_all(db_session):
    """update_files, then query all Movie, it must return some records"""
    update_files(db_session, SAMPLE_LIB, True)
    assert len(Movie.all(db_session)) >= 5


def test_get_by_tag(db_session):
    """update_files, then query all Movie by Tag, return matched Movies """
    update_files(db_session, SAMPLE_LIB, True)
    assert len(Movie.get_by_tag("forest", db_session)) == 2
    assert len(Movie.get_by_tag("non-exist-tag", db_session)) == 0


def test_get_by_actress(db_session):
    """update_files, then query all Movie by Actress, return matched Movies """
    update_files(db_session, SAMPLE_LIB, True)
    assert len(Movie.get_by_actress("L03BHPEH9SNKO", db_session)) == 5
    assert len(Movie.get_by_actress("non-exist-tag", db_session)) == 0


# tag

def test_tag_all(db_session):
    """update_files, then query all Tag, it must return some records"""
    update_files(db_session, SAMPLE_LIB, True)
    assert len(Tag.all(db_session)) >= 5


def test_get_by_movie(db_session):
    """update_files, then query all Tag by Movie, return matched Tags """
    update_files(db_session, SAMPLE_LIB, False)
    assert len(Tag.get_by_movie("L03BG2NLRKV5A", db_session)) == 2
    assert len(Tag.get_by_movie("non-exist-tag", db_session)) == 0
