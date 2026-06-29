"""manipulate perch.db with sqlalchemy, parse metadata with eagle_metaparser.py"""
import logging
import threading
from sqlalchemy.ext.declarative import declarative_base
from perch.parser.eagle import parse_actress_name_id, parse_all_file_metadatas
from perch.db.connection import Actress, Tag, Movie, Book

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
                meta = parse_all_file_metadatas()
                update_actress(self.session)
                update_newfiles(self.session, meta)
                update_tags(self.session, meta)
                update_count(self.session)
            finally:
                logging.info("DB update done!")


def update_actress(session):
    """check metadata.json and update DB actress table"""
    on_db_actresses_dict = {a.name: a.actressid
                            for a in session.query(Actress).all()}

    json_name_id_dict = parse_actress_name_id()
    target_actress = json_name_id_dict.keys() - on_db_actresses_dict.keys()

    if target_actress != []:
        target = [Actress(name=name, actressid=actressid)
                  for name, actressid in json_name_id_dict.items() if name in target_actress]
        session.add_all(target)
        session.commit()
        logging.debug("  [DEBUG][DB][actress] %s", target)


def update_tags(session, meta=None):
    """used in update_files, update tag datas"""
    if meta is None:
        meta = parse_all_file_metadatas()
    json_tag_set = set([t
                       for d in meta for _, v in d.items() for t in v["tags"]])
    on_db_tags_set = set([t.tag for t in session.query(Tag).all()])

    target_tags = json_tag_set - on_db_tags_set

    targets = [Tag(fileid=k, tag=t)
               for d in meta for k, v in d.items() for t in v["tags"] if t in target_tags]
    session.add_all(targets)
    session.commit()


def update_filename(session, movs, item):
    """file exist, update required?"""
    for mov in movs:
        if mov.filename != item["filename"]:
            logging.info(
                "file name changed ! %s -> %s", mov.filename, item['filename'])
            mov.filename = item["filename"]
            session.commit()


def update_newfiles(session, meta=None):
    """check images/metadata.json and update DB movie,tag table"""
    if meta is None:
        meta = parse_all_file_metadatas()

    json_fileids = set(
        [fileid for d in meta for fileid, _ in d.items()])

    on_db_movies_dict = {
        m.fileid: m.filename for m in session.query(Movie).all()}

    target_movies_set = json_fileids - on_db_movies_dict.keys()

    if target_movies_set == []:
        return

    targets_dicts = {k: v for d in meta
                     for k, v in d.items()
                     if k in target_movies_set}

    # FIXME アイテムを多重登録している
    targets = [Movie(fileid=k, filename=v["filename"],
                     actressid=i)
               for k, v in targets_dicts.items()
               for i in v["actressid"]]
    session.add_all(targets)
    session.commit()


def update_count(session):
    """check all actress data and set count number"""
    actresses = Actress.all(session)
    targets = []
    for actress in actresses:
        actress.count = Movie.count_by_actress(actress.actressid, session)
        logging.debug("  [DEBUG][DB][count] %s : %s",
                      actress.name, actress.count)

        first_movie = Movie.get_first_by_actress(actress.actressid, session)
        if first_movie is not None:
            actress.facepath = f"{first_movie.fileid}.info/{first_movie.filename}_thumbnail.png"
        else:
            actress.facepath = ""
        logging.debug("  [DEBUG][DB][facepath] %s", actress.facepath)

        targets.append(actress)
    session.add_all(targets)
    session.commit()


def drop_db(session):
    """drop all DB tables"""
    session.query(Actress).delete()
    session.query(Movie).delete()
    session.query(Book).delete()
    session.query(Tag).delete()
    session.commit()
    logging.warn("DB droped!")


# ── Book library sync ──────────────────────────────────

def update_books_from_lib(lib_path, session):
    """Scan eagle book library at lib_path and upsert into book table.
    Also adds tags with target_type='book'."""
    meta = parse_all_file_metadatas(lib_path)
    if not meta:
        logging.info("update_books_from_lib: no metadata found in %s", lib_path)
        return

    json_fileids = set(fileid for d in meta for fileid in d.keys())
    on_db = {b.fileid: b for b in session.query(Book).all()}
    new_ids = json_fileids - set(on_db.keys())

    # Upsert books
    for d in meta:
        for fileid, info in d.items():
            name = info.get("filename", "")
            ext = info.get("ext", "pdf")
            size = info.get("size", 0)
            mtime = info.get("mtime", 0)
            if fileid in on_db:
                b = on_db[fileid]
                b.name = name
                b.ext = ext
                b.size = size
                b.updated_at = mtime
            else:
                session.add(Book(
                    name=name, fileid=fileid, ext=ext,
                    size=size, created_at=mtime, updated_at=mtime,
                ))
    session.commit()
    logging.info("update_books_from_lib: %d books total (%d new)",
                 len(json_fileids), len(new_ids))

    # Sync tags (target_type='book')
    all_tags = set()
    for d in meta:
        for info in d.values():
            for t in info.get("tags", []):
                all_tags.add(t)
    on_db_tags = {t.tag for t in session.query(Tag).filter(
        Tag.target_type == "book").all()}
    new_tags = all_tags - on_db_tags
    for d in meta:
        for info in d.values():
            for t in info.get("tags", []):
                if t in new_tags:
                    session.add(Tag(fileid=fileid, tag=t, target_type="book"))
    # Note: we don't delete stale book tags — keep it simple
    session.commit()
    logging.info("update_books_from_lib: %d book tags (%d new)",
                 len(all_tags), len(new_tags))
