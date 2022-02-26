"""import pytest, sqlalchemy, app.perchdb, tests.conftest for CONST"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database
from app.perchdb import Base, Actress, update_actress
from tests.conftest import SAMPLE_LIB

DBPATH = 'sqlite:///tests/perch.db'


@pytest.fixture(name="db_session")
def fixture_db():
    """generate test DB(when test finished,DB file will be erased)"""
    test_engine = create_engine(DBPATH)
    test_session = sessionmaker(test_engine)

    # create DB tables inherited Base
    Base.metadata.create_all(test_engine)
    # return Session(), and wait test case finish
    yield test_session()

    # remove db file
    drop_database(DBPATH)


def test_update_actress(db_session):
    """parse master metadata.json, update DB actress table"""
    update_actress(db_session, SAMPLE_LIB, True)


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
