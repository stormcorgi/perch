"""manipulate perch.db with sqlalchemy, parse metadata with eagle_metaparser.py"""
import logging
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy import distinct
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def generate_engine(file_path):
    """require file_path(/some/path/dbname.sqlite)"""
    logging.debug(
        "engine generate -> sqlite:///%s?check_same_thread=False", file_path)
    return create_engine(
        f"sqlite:///{file_path}?check_same_thread=False")


def generate_session(file_path):
    "db_session""return Session"""
    return sessionmaker(generate_engine(file_path))


def init_db(file_path):
    """init db with app_context"""
    logging.debug("start init_db on %s", file_path)
    engine = generate_engine(file_path)
    # create DB tables inherited Base
    Base.metadata.create_all(engine)

    # ── lightweight migrations ──────────────────────────
    # tag.target_type (movie|book) — add if missing
    from sqlalchemy import inspect as _insp, text as _text
    cols = [c["name"] for c in _insp(engine).get_columns("tag")]
    if "target_type" not in cols:
        logging.info("migrating: add tag.target_type")
        with engine.connect() as conn:
            conn.execute(
                _text("ALTER TABLE tag ADD COLUMN target_type TEXT DEFAULT 'movie'")
            )
            conn.commit()
    # backfill existing rows (NULL → 'movie')
    with engine.connect() as conn:
        conn.execute(
            _text("UPDATE tag SET target_type='movie' WHERE target_type IS NULL")
        )
        conn.commit()


class Actress(Base):
    """table Actress : id, actressid, name"""
    __tablename__ = 'actress'
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
    __tablename__ = 'movie'
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
        tag_records = session.query(Tag).filter(
            Tag.tag == search_tag).all()
        for tag_record in tag_records:
            movies.append(session.query(cls).filter(
                cls.fileid == tag_record.fileid).first())
        return movies

    @classmethod
    def get_by_actress(cls, actressid, session):
        """Query DB, return all Movie that actress appear"""
        return session.query(cls).filter(
            cls.actressid == actressid).all()

    @classmethod
    def get_first_by_actress(cls, actressid, session):
        """Query DB, return first Movie that actress appear"""
        return session.query(cls).filter(cls.actressid == actressid).first()

    @classmethod
    def count_by_actress(cls, search_actressid, session):
        """return specified Actress's Movie count in DB"""
        return session.query(cls).filter(cls.actressid == search_actressid).count()

    @classmethod
    def get_by_fileid(cls, search_fileid, session):
        """Query Movie table and filter by fileid and return one Movie object"""
        return session.query(cls).filter(cls.fileid == search_fileid).first()

    @classmethod
    def get_by_id(cls, search_id, session):
        """Query Movie table and filter by id(not fileid) and return one Movie object"""
        return session.query(cls).filter(cls.id == search_id).first()


class Tag(Base):
    """table Tag : tagid, fileid, tag, target_type"""
    __tablename__ = 'tag'
    tagid = Column(Integer, primary_key=True, unique=True)
    fileid = Column(String)
    tag = Column(String)
    target_type = Column(String, default="movie")  # 'movie' | 'book'

    def __init__(self, fileid="", tag="", target_type="movie"):
        self.fileid = fileid
        self.tag = tag
        self.target_type = target_type

    def __repr__(self):
        return f"Tag<{self.tagid},{self.fileid},{self.tag}>"

    @classmethod
    def all(cls, session, target_type=None):
        """Query Tag table and make unique, then return all unique Tag object with count.
        If target_type given ('movie'|'book'), filter only those."""
        from sqlalchemy import func
        q = session.query(cls.tag, func.count(cls.fileid).label("count"))
        if target_type:
            q = q.filter(cls.target_type == target_type)
        tag_rows = q.group_by(cls.tag).order_by(cls.tag).all()
        tag_obj_list = []
        for tag_str, cnt in tag_rows:
            t = cls(0, tag_str)
            t.count = cnt
            tag_obj_list.append(t)
        return tag_obj_list

    @classmethod
    def get_by_movie(cls, fileid, session):
        """Query Tag table by Movie.fileid and return Tag object lists"""
        return session.query(cls).filter(cls.fileid == fileid).all()

    @classmethod
    def add_for_movie(cls, fileid, tag, session):
        """Add a tag for a movie if not already exists. Returns True if newly added, False if already existed."""
        existing = session.query(cls).filter(
            cls.fileid == fileid, cls.tag == tag).first()
        if not existing:
            t = cls(fileid=fileid, tag=tag)
            session.add(t)
            session.commit()
            return True
        return False

    @classmethod
    def remove_for_movie(cls, fileid, tag, session):
        """Remove a tag for a movie"""
        session.query(cls).filter(
            cls.fileid == fileid, cls.tag == tag).delete()
        session.commit()


class Book(Base):
    """table Book : id, name, fileid, ext, page_count, size, created_at, updated_at"""
    __tablename__ = 'book'
    id         = Column(Integer, primary_key=True, unique=True)
    name       = Column(String)
    fileid     = Column(String, unique=True)
    ext        = Column(String, default="pdf")
    page_count = Column(Integer, default=0)
    size       = Column(Integer, default=0)
    created_at = Column(Integer, default=0)  # unix ms
    updated_at = Column(Integer, default=0)  # unix ms

    def __repr__(self):
        return f"Book<{self.id},{self.name},{self.fileid},{self.ext}>"

    @classmethod
    def all(cls, session):
        return session.query(cls).order_by(cls.name).all()

    @classmethod
    def count_all(cls, session):
        return session.query(cls).count()

    @classmethod
    def get_by_fileid(cls, search_fileid, session):
        return session.query(cls).filter(cls.fileid == search_fileid).first()

    @classmethod
    def get_by_id(cls, search_id, session):
        return session.query(cls).filter(cls.id == search_id).first()

    @classmethod
    def get_by_tag(cls, search_tag, session):
        books = []
        tag_records = session.query(Tag).filter(
            Tag.tag == search_tag, Tag.target_type == "book").all()
        for tag_record in tag_records:
            books.append(session.query(cls).filter(
                cls.fileid == tag_record.fileid).first())
        return books

    @classmethod
    def add_or_update(cls, session, *, name, fileid, ext="pdf",
                      page_count=0, size=0, created_at=0, updated_at=0):
        """Insert or update a book row by fileid (upsert)."""
        existing = session.query(cls).filter(cls.fileid == fileid).first()
        if existing:
            existing.name = name
            existing.ext = ext
            existing.page_count = page_count
            existing.size = size
            existing.created_at = created_at
            existing.updated_at = updated_at
            session.commit()
            return existing
        b = cls(name=name, fileid=fileid, ext=ext,
                page_count=page_count, size=size,
                created_at=created_at, updated_at=updated_at)
        session.add(b)
        session.commit()
        return b
