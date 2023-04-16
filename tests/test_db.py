"""import pytest, sqlalchemy, app.perchdb, tests.conftest for CONST"""
import pytest
from sqlalchemy.orm import sessionmaker

from perch.db.connection import Actress, Base, Movie, Tag, generate_engine
from perch.db.update import drop_db, update_actress, update_newfiles, update_tags


@pytest.fixture(name="db_session")
def fixture_db(app):
    """generate test DB(when test finished,DB file will be erased)"""
    with app.app_context():
        test_engine = generate_engine(app.config["DATABASE"])
        test_session = sessionmaker(test_engine)
        # create DB tables inherited Base
        Base.metadata.create_all(test_engine)
        # return Session(), and wait test case finish
        yield test_session()


# general


def test_update_actress(db_session):
    """parse master metadata.json, update DB actress table"""
    drop_db(db_session)
    assert len(db_session.query(Actress).all()) == 0
    update_actress(db_session)
    assert len(db_session.query(Actress).all()) >= 1
    update_actress(db_session)
    assert len(db_session.query(Actress).all()) >= 1


def test_update_newfiles(db_session):
    """parse each file's metadata.json, update DB file,tag table"""
    drop_db(db_session)
    assert len(db_session.query(Movie).all()) == 0
    update_newfiles(db_session)
    assert len(db_session.query(Movie).all()) != 0


def test_drop_db(db_session):
    """test dropping db"""
    update_actress(db_session)
    update_newfiles(db_session)
    assert len(db_session.query(Actress).all()) >= 1
    assert len(db_session.query(Movie).all()) != 0
    drop_db(db_session)
    assert len(db_session.query(Actress).all()) == 0
    assert len(db_session.query(Movie).all()) == 0


# actress


def test_actress_all(db_session):
    """return all Actress data query-able"""
    update_actress(db_session)
    all_actresses = Actress.all(db_session)
    for actress in all_actresses:
        assert isinstance(actress.id, int) is True
        assert isinstance(actress.actressid, str) is True
        assert isinstance(actress.name, str) is True


def test_actress_get_by_name(db_session):
    """query by name string"""
    update_actress(db_session)
    record = Actress.get_by_name("food", db_session)
    assert record is not None
    assert record.id == 3
    assert record.actressid == "L03BHCN6FV119"
    assert record.name == "food"
    record = Actress.get_by_name("non-exist-name", db_session)
    assert record is None


def test_actress_get_by_id(db_session):
    """query by actressid , return Actress object"""
    update_actress(db_session)
    assert isinstance(Actress.get_by_id("L03BHCN6FV119", db_session), Actress)
    assert Actress.get_by_id("non-exist-actressid", db_session) is None


def test_actress_get_by_movie(db_session):
    """query Movie table by fileid, return all Actress object"""
    update_actress(db_session)
    update_newfiles(db_session)
    movies = Actress.get_by_movie("L03BG2NK1ERKW", db_session)
    assert len(movies) == 2
    for movie in movies:
        assert isinstance(movie, Actress)


# movie


def test_movie_all(db_session):
    """update_files, then query all Movie, it must return some records"""
    update_newfiles(db_session)
    assert len(Movie.all(db_session)) >= 5


def test_get_by_tag(db_session):
    """update_files, then query all Movie by Tag, return matched Movies"""
    update_actress(db_session)
    update_newfiles(db_session)
    update_tags(db_session)
    assert len(Movie.get_by_tag("forest", db_session)) == 2
    assert len(Movie.get_by_tag("non-exist-tag", db_session)) == 0


def test_get_by_actress(db_session):
    """update_files, then query all Movie by Actress, return matched Movies"""
    update_newfiles(db_session)
    assert len(Movie.get_by_actress("L03BHPEH9SNKO", db_session)) == 5
    assert len(Movie.get_by_actress("non-exist-tag", db_session)) == 0


def test_get_by_id(db_session):
    """query by int: id(not actress id)"""
    update_newfiles(db_session)
    assert isinstance(Movie.get_by_id(3, db_session), Movie)
    assert isinstance(Movie.get_by_id(99999, db_session), Movie) is False


def test_count_all(db_session):
    """COUNT query"""
    update_newfiles(db_session)
    assert Movie.count_all(db_session) >= 5


def test_count_by_actress(db_session):
    """count by actressid"""
    update_newfiles(db_session)
    assert Movie.count_by_actress("L03BHPEH9SNKO", db_session) == 5
    assert Movie.count_by_actress("non-exist-tag", db_session) == 0


# tag


def test_tag_all(db_session):
    """update_files, then query all Tag, it must return some records"""
    update_newfiles(db_session)
    update_tags(db_session)
    assert len(Tag.all(db_session)) >= 5


def test_get_by_movie(db_session):
    """update_files, then query all Tag by Movie, return matched Tags"""
    update_newfiles(db_session)
    update_tags(db_session)
    assert len(Tag.get_by_movie("L03BG2NLRKV5A", db_session)) == 2
    assert len(Tag.get_by_movie("non-exist-tag", db_session)) == 0
