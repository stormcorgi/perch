"""load perch.db"""
from flask.cli import with_appcontext
from perch.db import Actress, Movie, Tag
from perch.db import init_db, update_actress, update_files, update


def test_update_actress(app):
    """parse master metadata.json, update DB actress table"""
    with app.app_context():
        init_db()
        update_actress()


# def test_update_files(app):
#     """parse each file's metadata.json, update DB file,tag table"""
#     with app.app_context():
#         update_files()
#
#
# def test_update(app):
#     """parse each file's metadata.json, update DB file,tag table"""
#     with app.app_context():
#         update()
# actress


# def test_actress_all(app):
#     """return all Actress data query-able"""
#     with app.app_context():
#         update_actress()
#         all_actresses = Actress.all()
#         for actress in all_actresses:
#             print(actress.id)
#             assert isinstance(actress.id, int) is True
#             assert isinstance(actress.actressid, str) is True
#             assert isinstance(actress.name, str) is True


# def test_actress_get_by_name(app):
#     """query by name string"""
#     with app.app_context():
#         update()
#         record = Actress.get_by_name("food")
#         assert record is not None
#         if record is not None:
#             print(f"{record.id} {record.actressid} {record.name}")
#             assert record.id == 3
#             assert record.actressid == "L03BHCN6FV119"
#             assert record.name == "food"
#
#         assert Actress.get_by_name("non-exist-name") is None
#
#
# def test_actress_get_by_id(app):
#     """query by actressid , return Actress object"""
#     with app.app_context():
#         update_actress()
#         assert isinstance(Actress.get_by_id("L03BHCN6FV119"), Actress)
#         assert Actress.get_by_id("non-exist-actressid") is None
#
#
# def test_actress_get_by_movie(app):
#     """query Movie table by fileid, return all Actress object"""
#     with app.app_context():
#         update_actress()
#         update_files()
#         movies = Actress.get_by_movie("L03BG2NK1ERKW")
#         assert len(movies) == 2
#         for movie in movies:
#             assert isinstance(movie, Actress)
#
# # movie
#
#
# def test_movie_all(app):
#     """update_files, then query all Movie, it must return some records"""
#     with app.app_context():
#         update_files()
#         assert len(Movie.all()) >= 5
#
#
# def test_get_by_tag(app):
#     """update_files, then query all Movie by Tag, return matched Movies """
#     with app.app_context():
#         update_files()
#         assert len(Movie.get_by_tag("forest")) == 2
#         assert len(Movie.get_by_tag("non-exist-tag")) == 0
#
#
# def test_get_by_actress(app):
#     """update_files, then query all Movie by Actress, return matched Movies """
#     with app.app_context():
#         update_files()
#         assert len(Movie.get_by_actress("L03BHPEH9SNKO")) == 5
#         assert len(Movie.get_by_actress("non-exist-tag")) == 0
#
#
# # tag
#
# def test_tag_all(app):
#     """update_files, then query all Tag, it must return some records"""
#     with app.app_context():
#         update_files()
#         assert len(Tag.all()) >= 5
#
#
# def test_get_by_movie(app):
#     """update_files, then query all Tag by Movie, return matched Tags """
#     with app.app_context():
#         update_files()
#         assert len(Tag.get_by_movie("L03BG2NLRKV5A")) == 2
#         assert len(Tag.get_by_movie("non-exist-tag")) == 0
