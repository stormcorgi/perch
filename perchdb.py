from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from eagle_metaparser import *

engine = create_engine('sqlite:///perch.db')
Base = declarative_base()
Session = sessionmaker(engine)

class Actress(Base):
    __tablename__ = 'actress'
    id = Column(Integer, primary_key=True, unique=True)
    actressid = Column(String)
    name = Column(String)

    def __repr__(self):
        return "Actress<{},{},{}>".format(self.id,self.actressid,self.name)

class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True, unique=True)
    fileid = Column(String)
    filename = Column(String)
    actressid = Column(String)

    def __repr__(self):
        return "Movie<{},{},{}>".format(self.id,self.filename,self.fileid)

## create DB tables inherited Base
Base.metadata.create_all(engine)

def get_actressdata_by_name(name) :
    with Session() as session:
        actress = session.query(Actress).filter(Actress.name == name).first()
    return actress
    
def get_actresses() :
    with Session() as session:
        actresses = session.query(Actress).all()
    return actresses

def update_actress():
    with Session() as session:
        name_id_lists = get_actress_name_id()
        for k, v in name_id_lists.items():
            print("=== " + k + " ===")
            print("id : " + v)
            a = Actress(name=k,actressid=v)
            session.add(a)
            session.commit()

def update_files():
    with Session() as session:
        lists = get_all_file_metadatas()
        for lst in lists:
            for k,v in lst.items():
                for i in v["actressid"]:
                    print("=== fileid : " +  k + " ===")
                    print(" " + v["filename"])
                    print(" - actress - > " + i)
                    m = Movie(fileid=k,filename=v["filename"],actressid=i)
                    session.add(m)
                    session.commit()

def get_movies_by_actressid(actressid):
    with Session() as session:
        movies = session.query(Movie).filter(Movie.actressid == actressid).all()
    return movies

def get_movies():
    with Session() as session:
        movies = session.query(Movie).all()
    return movies


if __name__ == "__main__":
    update_actress()
    update_files()