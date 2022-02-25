from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy import distinct
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from eagle_metaparser import get_actress_name_id, get_all_file_metadatas

engine = create_engine('sqlite:///perch.db')
Base = declarative_base()
Session = sessionmaker(engine)


class Actress(Base):
    __tablename__ = 'actress'
    id = Column(Integer, primary_key=True, unique=True)
    actressid = Column(String)
    name = Column(String)

    def __repr__(self):
        return "Actress<{},{},{}>".format(self.id, self.actressid, self.name)


class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True, unique=True)
    filename = Column(String)
    fileid = Column(String)
    actressid = Column(String)

    def __repr__(self):
        return "Movie<{},{},{},{}>".format(
            self.id, self.filename, self.fileid, self.actressid)


class Tag(Base):
    __tablename__ = 'tag'
    tagid = Column(Integer, primary_key=True, unique=True)
    fileid = Column(String)
    tag = Column(String)

    def __init__(self, fileid, tag):
        self.fileid = fileid
        self.tag = tag

    def __repr__(self):
        return "Tag<{},{},{}>".format(self.tagid, self.fileid, self.tag)


# create DB tables inherited Base
Base.metadata.create_all(engine)


def get_actressdata_by_name(name):
    with Session() as session:
        actress = session.query(Actress).filter(Actress.name == name).first()
    return actress


def get_movies_by_tag(tag):
    movies = []
    with Session() as session:
        tags = session.query(Tag).filter(Tag.tag == tag).all()
        for t in tags:
            movies.append(session.query(Movie).filter(
                Movie.fileid == t.fileid).first())
    return movies


def get_tags_by_movie(fileid):
    with Session() as session:
        return session.query(Tag).filter(Tag.fileid == fileid).all()


def get_actresses():
    with Session() as session:
        actresses = session.query(Actress).all()
    return actresses


def get_tags():
    tagList = []
    with Session() as session:
        tags = session.query(distinct(Tag.tag)).all()
        # rawTags = session.query(Tag).all()
    for tag in tags:
        # print("Tag<-,-,%s>" % (tag[0]))
        tagList.append(Tag(0, tag[0]))
    return tagList


def update_actress():
    with Session() as session:
        name_id_lists = get_actress_name_id()
        for k, v in name_id_lists.items():
            act = session.query(Actress).filter(Actress.actressid == v).all()
            if not act:
                print("=== " + k + " ===")
                print("id : " + v)
                a = Actress(name=k, actressid=v)
                session.add(a)
                session.commit()


def update_files():
    with Session() as session:
        lists = get_all_file_metadatas()
        for lst in lists:
            for k, v in lst.items():
                # put tag DB to fileid
                for tag in v["tags"]:
                    # if tag is already exist, pass
                    # FIXME if tag deleted, record still exist...
                    currentTags = session.query(Tag).filter(
                        Tag.fileid == k, Tag.tag == tag).all()
                    if not currentTags:
                        t = Tag(fileid=k, tag=tag)
                        session.add(t)
                        session.commit()

                # FIXME each actressid, put movie record. strange SQL usage?
                for i in v["actressid"]:
                    # if data is already exist(fileid AND actressid), pass
                    mov = session.query(Movie).filter(
                        Movie.fileid == k, Movie.actressid == i).all()
                    if not mov:
                        print("=== fileid : " + k + " ===")
                        print(" " + v["filename"])
                        print(" - actress - > " + i)
                        print(" - tags - ")
                        print(v["tags"])
                        m = Movie(
                            fileid=k, filename=v["filename"], actressid=i)
                        session.add(m)
                        session.commit()
                    else:
                        # file exist, update required?
                        for m in mov:
                            if m.filename != v["filename"]:
                                print("file name changed ! %s -> %s" %
                                      (m.filename, v["filename"]))
                                m.filename = v["filename"]
                                session.commit()


def get_movies_by_actressid(actressid):
    with Session() as session:
        movies = session.query(Movie).filter(
            Movie.actressid == actressid).all()
    return movies


def get_movies():
    with Session() as session:
        movies = session.query(Movie).all()
    return movies


if __name__ == "__main__":
    update_actress()
    update_files()
    # print(get_movies_by_tag("480p"))
    # print(get_tags_by_movie("KYCDXFAFR3R5F"))
