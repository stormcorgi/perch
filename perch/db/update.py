"""manipulate perch.db with sqlalchemy, parse metadata with eagle_metaparser.py"""
import logging
import threading
from sqlalchemy.ext.declarative import declarative_base
from perch.parser.eagle import parse_actress_name_id, parse_all_file_metadatas
from perch.db.connection import Actress, Tag, Movie

Base = declarative_base()


class UpdateThread(threading.Thread):
    """ for execute update_db on background(another thread) """

    def __init__(self, app, session):
        super(UpdateThread, self).__init__()
        self.stop_event = threading.Event()
        self.app = app
        self.session = session

    def stop(self):
        """ stop update_db on another thread"""
        self.stop_event.set()

    def run(self):
        with self.app.app_context():
            try:
                update_actress(self.session)
                update_files(self.session)
                update_count(self.session)
            finally:
                logging.info("DB update done!")


def update_actress(session):
    """check metadata.json and update DB actress table"""
    name_id_lists = parse_actress_name_id()
    for name, actressid in name_id_lists.items():
        act = session.query(Actress).filter(
            Actress.actressid == actressid).all()
        if not act:
            logging.debug("%s : %s", name, actressid)
            actress_sql = Actress(name=name, actressid=actressid)
            session.add(actress_sql)
            session.commit()
            logging.debug("  [DEBUG][DB][actress] %s", actress_sql)


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
            logging.debug("  [DEBUG][DB][tags] %s", tag_sql)


def update_filename(session, movs, item):
    """file exist, update required?"""
    for mov in movs:
        if mov.filename != item["filename"]:
            logging.info(
                "file name changed ! %s -> %s", mov.filename, item['filename'])
            mov.filename = item["filename"]
            session.commit()


def update_files(session):
    """check images/metadata.json and update DB movie,tag table"""
    lists = parse_all_file_metadatas()
    for lst in lists:
        logging.debug(" [DEBUG] lst = %s", lst)
        try:
            lst.items()
        except AttributeError as attribute_e:
            logging.warning(" [WARNING] Attribute Error occured on %s", lst)
            logging.warning(" [WARNING] %s", attribute_e)
            continue

        for fileid, item in lst.items():
            update_tags(session, fileid, item)

            # TODO each actressid, put movie record. strange SQL usage?
            for i in item["actressid"]:
                # if data is already exist(fileid AND actressid), pass
                movs = session.query(Movie).filter(
                    Movie.fileid == fileid, Movie.actressid == i).all()
                if not movs:
                    logging.debug("id : %s ", fileid)
                    logging.debug(" - filename - > %s", item["filename"])
                    logging.debug(" - actress -- > %s", i)
                    logging.debug(" - tags - ")
                    logging.debug("    - %s", item["tags"])
                    mov_sql = Movie(
                        fileid=fileid, filename=item["filename"], actressid=i)
                    session.add(mov_sql)
                    session.commit()
                    logging.debug("  [DEBUG][DB][files] %s", mov_sql)
                else:
                    update_filename(session, movs, item)


def update_count(session):
    """check all actress data and set count number"""
    actresses = Actress.all(session)
    for actress in actresses:
        actress.count = Movie.count_by_actress(actress.actressid, session)
        logging.debug("  [DEBUG][DB][count] %s", actress.count)

        first_movie = Movie.get_first_by_actress(actress.actressid, session)
        actress.facepath = f"{first_movie.fileid}.info/{first_movie.filename}_thumbnail.png"
        logging.debug("  [DEBUG][DB][facepath] %s", actress.facepath)

        session.commit()


def drop_db(session):
    """drop all DB tables"""
    session.query(Actress).delete()
    session.query(Movie).delete()
    session.query(Tag).delete()
    session.commit()
