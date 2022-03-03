"""manipulate perch.db with sqlalchemy, parse metadata with eagle_metaparser.py"""
import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy import distinct
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from perch.eagle_metaparser import parse_actress_name_id, parse_all_file_metadatas

base = declarative_base()


@with_appcontext
def get_db_engine():
    """return db session, see current_app.config["databse"]"""
    db_path = current_app.config["DATABASE"]
    lib_path = current_app.config["LIB_PATH"]
    print(f"db_path -> {db_path}, lib_path -> {lib_path}")
    return create_engine(
        f"sqlite:///{db_path}?check_same_thread=False")


def init_db():
    """create DB tables inherited Base"""
    engine = get_db_engine()
    base.metadata.create_all(engine)


Session = sessionmaker(get_db_engine())
connection = Session()


class Actress(base):
    """table Actress : id, actressid, name"""
    __tablename__ = 'actress'
    id = Column(Integer, primary_key=True, unique=True)
    actressid = Column(String)
    name = Column(String)

    def __repr__(self):
        return f"Actress<{self.id},{self.actressid},{self.name}>"

    @classmethod
    def all(cls):
        """Query Actress table and return all Actress object"""
        return connection.query(cls).all()

    @classmethod
    def get_by_name(cls, name):
        """Query Actress table and filter by name and return one Actress object"""
        return connection.query(cls).filter(cls.name == name).first()

    @classmethod
    def get_by_id(cls, actressid):
        """Query Actress table and filter by actressid and return one Actress object"""
        return connection.query(cls).filter(cls.actressid == actressid).first()

    @classmethod
    def get_by_movie(cls, fileid):
        """Query Movie table and filter by fileid and return all Actresses object"""
        movie_obj_list = []
        movies = connection.query(Movie).filter(Movie.fileid == fileid).all()
        for movie in movies:
            movie_obj_list.append(cls.get_by_id(movie.actressid))
        return movie_obj_list


class Movie(base):
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
        return connection.query(cls).all()

    @classmethod
    def get_by_tag(cls, search_tag):
        """Query Tag table by tag and return Movie object lists"""
        movies = []
        tag_records = connection.query(Tag).filter(
            Tag.tag == search_tag).all()
        for tag_record in tag_records:
            movies.append(connection.query(cls).filter(
                cls.fileid == tag_record.fileid).first())
        return movies

    @classmethod
    def get_by_actress(cls, actressid):
        """Query DB, return all Movie that actress appear"""
        return connection.query(cls).filter(
            cls.actressid == actressid).all()


class Tag(base):
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
        tag_obj_list = []
        tag_str_list = []
        tags_str = connection.query(distinct(cls.tag)).all()
        for tag_str in tags_str:
            tag_str_list.append(tag_str[0])
        tag_str_list = sorted(tag_str_list)
        for tag_str in tag_str_list:
            tag_obj_list.append(cls(0, tag_str))
        return tag_obj_list

    @classmethod
    def get_by_movie(cls, fileid):
        """Query Tag table by Movie.fileid and return Tag object lists"""
        return connection.query(cls).filter(cls.fileid == fileid).all()


def update_actress():
    """check metadata.json and update DB actress table"""
    name_id_lists = parse_actress_name_id()
    print(name_id_lists)
    for name, actressid in name_id_lists.items():
        act = connection.query(Actress).filter(
            Actress.actressid == actressid).all()
        if not act:
            # if not quiet:
            print("=== " + name + " ===")
            print("id : " + actressid)
            actress_sql = Actress(name=name, actressid=actressid)
            connection.add(actress_sql)
            connection.commit()


def update_tags(fileid, item):
    """used in update_files, update tag datas"""
    # put tag DB to fileid
    for tag in item["tags"]:
        # if tag is already exist, pass
        # TODO if tag deleted, record still exist...
        current_tags = connection.query(Tag).filter(
            Tag.fileid == fileid, Tag.tag == tag).all()
        if not current_tags:
            tag_sql = Tag(fileid=fileid, tag=tag)
            connection.add(tag_sql)
            connection.commit()


def update_filename(movs, item):
    """file exist, update required?"""
    for mov in movs:
        if mov.filename != item["filename"]:
            print(
                f"file name changed ! {mov.filename} -> {item['filename']}")
            mov.filename = item["filename"]
            connection.commit()


def update_files():
    """check images/metadata.json and update DB movie,tag table"""
    lists = parse_all_file_metadatas()
    for lst in lists:
        for fileid, item in lst.items():
            update_tags(fileid, item)

            # TODO each actressid, put movie record. strange SQL usage?
            for i in item["actressid"]:
                # if data is already exist(fileid AND actressid), pass
                movs = connection.query(Movie).filter(
                    Movie.fileid == fileid, Movie.actressid == i).all()
                if not movs:
                    # if not quiet:
                    #     print("=== fileid : " + fileid + " ===")
                    #     print(" - filename - > " + item["filename"])
                    #     print(" - actress -- > " + i)
                    #     print(" - tags - ")
                    #     print(item["tags"])
                    mov_sql = Movie(
                        fileid=fileid, filename=item["filename"], actressid=i)
                    connection.add(mov_sql)
                    connection.commit()
                else:
                    update_filename(movs, item)


def update():
    """execute update_actress(), update_files()"""
    update_actress()
    update_files()


@click.command('update-db')
@with_appcontext
def update_db():
    """click command for update-db(flask update-db)"""
    init_db()
    update()
    click.echo("db updated")
    click.echo(Actress.all())
