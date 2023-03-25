"""manipulate perch.db with sqlalchemy, parse metadata with eagle_metaparser.py"""
import logging

from sqlalchemy import Column, Integer, String, create_engine, distinct
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def generate_engine(file_path):
    """require file_path(/some/path/dbname.sqlite)"""
    logging.debug("engine generate -> sqlite:///%s?check_same_thread=False", file_path)
    return create_engine(f"sqlite:///{file_path}?check_same_thread=False")


def generate_session(file_path):
    "db_session" "return Session" ""
    return sessionmaker(generate_engine(file_path))


def init_db(file_path):
    """init db with app_context"""
    logging.debug("start init_db on %s", file_path)
    engine = generate_engine(file_path)
    # create DB tables inherited Base
    Base.metadata.create_all(engine)


class Actress(Base):
    """table Actress : id, actressid, name"""

    __tablename__ = "actress"
    id = Column(Integer, primary_key=True, unique=True)
    actressid = Column(String)
    name = Column(String)
    count = Column(Integer)
    facepath = Column(String)

    def __repr__(self):
        return f"Actress<{self.id},{self.actressid},{self.name},{self.count},{self.facepath}>"

    @classmethod
    def all(cls, session):
        """Query Actress table and return all Actress object"""
        return session.query(cls).order_by(cls.name).all()

    @classmethod
    def get_by_name(cls, name, session):
        """Query Actress table and filter by name and return one Actress object"""
        return session.query(cls).filter(cls.name == name).first()

    @classmethod
    def get_by_id(cls, actressid, session):
        """Query Actress table and filter by actressid and return one Actress object"""
        return session.query(cls).filter(cls.actressid == actressid).first()

    @classmethod
    def get_by_movie(cls, fileid, session):
        """Query Movie table and filter by fileid and return all Actresses object"""
        movie_obj_list = []
        movies = session.query(Movie).filter(Movie.fileid == fileid).all()
        for movie in movies:
            movie_obj_list.append(cls.get_by_id(movie.actressid, session))
        return movie_obj_list


class Movie(Base):
    """table Movie : id, filename, fileid, actressid"""

    __tablename__ = "movie"
    id = Column(Integer, primary_key=True, unique=True)
    filename = Column(String)
    fileid = Column(String)
    actressid = Column(String)

    def __repr__(self):
        return f"Movie<{self.id},{self.filename},{self.fileid},{self.actressid}>"

    @classmethod
    def all(cls, session):
        """return all Movie in DB"""
        return session.query(cls).all()

    @classmethod
    def count_all(cls, session):
        """return all Movies count in DB"""
        return session.query(cls).count()

    @classmethod
    def get_by_tag(cls, search_tag, session):
        """Query Tag table by tag and return Movie object lists"""
        movies = []
        tag_records = session.query(Tag).filter(Tag.tag == search_tag).all()
        for tag_record in tag_records:
            movies.append(
                session.query(cls).filter(cls.fileid == tag_record.fileid).first()
            )
        return movies

    @classmethod
    def get_by_actress(cls, actressid, session):
        """Query DB, return all Movie that actress appear"""
        return session.query(cls).filter(cls.actressid == actressid).all()

    @classmethod
    def get_first_by_actress(cls, actressid, session):
        """Query DB, return first Movie that actress appear"""
        return session.query(cls).filter(cls.actressid == actressid).first()

    @classmethod
    def count_by_actress(cls, search_actressid, session):
        """return specified Actress's Movie count in DB"""
        return session.query(cls).filter(cls.actressid == search_actressid).count()

    @classmethod
    def get_by_id(cls, search_id, session):
        """Query Movie table and filter by id(not fileid) and return one Movie object"""
        return session.query(cls).filter(cls.id == search_id).first()


class Tag(Base):
    """table Tag : tagid, fileid, tag"""

    __tablename__ = "tag"
    tagid = Column(Integer, primary_key=True, unique=True)
    fileid = Column(String)
    tag = Column(String)

    def __init__(self, fileid="", tag=""):
        self.fileid = fileid
        self.tag = tag

    def __repr__(self):
        return f"Tag<{self.tagid},{self.fileid},{self.tag}>"

    @classmethod
    def all(cls, session):
        """Query Tag table and make unique, then return all unique Tag object"""
        tag_obj_list = []
        tag_str_list = []
        tags_str = session.query(distinct(cls.tag)).all()
        for tag_str in tags_str:
            tag_str_list.append(tag_str[0])
        tag_str_list = sorted(tag_str_list)
        for tag_str in tag_str_list:
            tag_obj_list.append(cls(0, tag_str))
        return tag_obj_list

    @classmethod
    def get_by_movie(cls, fileid, session):
        """Query Tag table by Movie.fileid and return Tag object lists"""
        return session.query(cls).filter(cls.fileid == fileid).all()
