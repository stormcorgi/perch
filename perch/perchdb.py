"""manipulate perch.db with sqlalchemy, parse metadata with eagle_metaparser.py"""
import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy import distinct
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from perch.eagle_metaparser import parse_actress_name_id, parse_all_file_metadatas

file_path = os.path.dirname(__file__)
LIB_PATH = f"{file_path}/../static/eagle_library"
engine = create_engine(
    f"sqlite:///{file_path}/../instance/perch.sqlite?check_same_thread=False")
Base = declarative_base()
Session = sessionmaker(engine)


def generate_session():
    """return Session"""
    return sessionmaker(engine)


class Actress(Base):
    """table Actress : id, actressid, name"""
    __tablename__ = 'actress'
    id = Column(Integer, primary_key=True, unique=True)
    actressid = Column(String)
    name = Column(String)

    def __repr__(self):
        return f"Actress<{self.id},{self.actressid},{self.name}>"

    @classmethod
    def all(cls, session):
        """Query Actress table and return all Actress object"""
        return session.query(cls).all()

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


class Tag(Base):
    """table Tag : tagid, fileid, tag"""
    __tablename__ = 'tag'
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


# create DB tables inherited Base
Base.metadata.create_all(engine)


def update_actress(session=Session(), lib_path=LIB_PATH, quiet=False):
    """check metadata.json and update DB actress table"""
    name_id_lists = parse_actress_name_id(lib_path)
    for name, actressid in name_id_lists.items():
        act = session.query(Actress).filter(
            Actress.actressid == actressid).all()
        if not act:
            if not quiet:
                print("=== " + name + " ===")
                print("id : " + actressid)
            actress_sql = Actress(name=name, actressid=actressid)
            session.add(actress_sql)
            session.commit()


def update_tags(session, fileid, item):
    """used in update_files, update tag datas"""
    # put tag DB to fileid
    for tag in item["tags"]:
        # if tag is already exist, pass
        # TODO if tag deleted, record still exist...
        current_tags = session.query(Tag).filter(
            Tag.fileid == fileid, Tag.tag == tag).all()
        if not current_tags:
            tag_sql = Tag(fileid=fileid, tag=tag)
            session.add(tag_sql)
            session.commit()


def update_filename(session, movs, item):
    """file exist, update required?"""
    for mov in movs:
        if mov.filename != item["filename"]:
            print(
                f"file name changed ! {mov.filename} -> {item['filename']}")
            mov.filename = item["filename"]
            session.commit()


def update_files(session=Session(), lib_path=LIB_PATH, quiet=False):
    """check images/metadata.json and update DB movie,tag table"""
    lists = parse_all_file_metadatas(lib_path)
    for lst in lists:
        for fileid, item in lst.items():
            update_tags(session, fileid, item)

            # TODO each actressid, put movie record. strange SQL usage?
            for i in item["actressid"]:
                # if data is already exist(fileid AND actressid), pass
                movs = session.query(Movie).filter(
                    Movie.fileid == fileid, Movie.actressid == i).all()
                if not movs:
                    if not quiet:
                        print("=== fileid : " + fileid + " ===")
                        print(" - filename - > " + item["filename"])
                        print(" - actress -- > " + i)
                        print(" - tags - ")
                        print(item["tags"])
                    mov_sql = Movie(
                        fileid=fileid, filename=item["filename"], actressid=i)
                    session.add(mov_sql)
                    session.commit()
                else:
                    update_filename(session, movs, item)


if __name__ == "__main__":
    update_actress()
    update_files()
