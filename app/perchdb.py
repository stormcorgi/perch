"""manipulate perch.db with sqlalchemy, parse metadata with eagle_metaparser.py"""
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy import distinct
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from eagle_metaparser import get_actress_name_id, get_all_file_metadatas

LIB_PATH = "./static/eagle.library"
engine = create_engine('sqlite:///database/perch.db')
Base = declarative_base()
Session = sessionmaker(engine)


class Actress(Base):
    """table Actress : id, actressid, name"""
    __tablename__ = 'actress'
    id = Column(Integer, primary_key=True, unique=True)
    actressid = Column(String)
    name = Column(String)

    def __repr__(self):
        return f"Actress<{self.id},{self.actressid},{self.name}>"

    @classmethod
    def all(cls, session=Session()):
        """Query Actress table and return all Actress object"""
        return session.query(cls).all()

    @classmethod
    def get_by_name(cls, name, session=Session()):
        """Query Actress table and filter by name and return one Actress object"""
        return session.query(cls).filter(cls.name == name).first()


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
    def all(cls):
        """return all Movie in DB"""
        with Session() as session:
            movies = session.query(cls).all()
        return movies

    @classmethod
    def get_by_tag(cls, search_tag):
        """Query Tag table by tag and return Movie object lists"""
        movies = []
        with Session() as session:
            tag_records = session.query(Tag).filter(
                Tag.tag == search_tag).all()
            for tag_record in tag_records:
                movies.append(session.query(cls).filter(
                    cls.fileid == tag_record.fileid).first())
        return movies

    @classmethod
    def get_by_actress(cls, actressid):
        """Query DB, return all Movie that actress appear"""
        with Session() as session:
            movies = session.query(cls).filter(
                cls.actressid == actressid).all()
        return movies


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
    def all(cls):
        """Query Tag table and make unique, then return all unique Tag object"""
        tag_list = []
        with Session() as session:
            tags = session.query(distinct(cls.tag)).all()
            # rawTags = session.query(Tag).all()
        for tag in tags:
            # print("Tag<-,-,%s>" % (tag[0]))
            tag_list.append(cls(0, tag[0]))
        return tag_list

    @classmethod
    def get_by_movie(cls, fileid):
        """Query Tag table by Movie.fileid and return Tag object lists"""
        with Session() as session:
            return session.query(cls).filter(cls.fileid == fileid).all()


# create DB tables inherited Base
Base.metadata.create_all(engine)


def update_actress(session=Session(), lib_path=LIB_PATH, quiet=False):
    """check metadata.json and update DB actress table"""
    name_id_lists = get_actress_name_id(lib_path)
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


def update_files(quiet=False):
    """check images/metadata.json and update DB movie,tag table"""
    with Session() as session:
        lists = get_all_file_metadatas()
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
                            print(" " + item["filename"])
                            print(" - actress - > " + i)
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
