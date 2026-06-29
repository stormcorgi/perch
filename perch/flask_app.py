""" use flask and perchdb.py """
import datetime
import glob
import logging
import os
import random
import threading
import unicodedata

import flask.app
from flask import Flask, jsonify, redirect, render_template, request, url_for, send_from_directory

import perch.db.connection as dbcon
import perch.db.update as dbup

start_dt = datetime.datetime.now()
start_str = start_dt.strftime("%Y%m%d")
logging.basicConfig(
    level=logging.INFO,
    filename=f"./log/perch-{start_str}.log",
    format="%(asctime)s %(message)s",
)


def create_app() -> flask.app.Flask:
    """Create and configure an instance of flask app"""
    app = Flask(__name__, instance_relative_config=True)

    config_type = {
        "development": "perch.config.Development",
        "testing": "perch.config.Testing",
        "production": "perch.config.Production",
    }
    logging.info("ENV : %s", os.getenv("FLASK_APP_ENV", "production"))

    app.config.from_object(config_type.get(os.getenv("FLASK_APP_ENV", "production")))

    logging.info("app generate start...")
    logging.debug("DB => %s", app.config["DATABASE"])
    logging.debug("LIB_PATH => %s", app.config["LIB_PATH"])

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db_full_path = os.path.join(app.instance_path, app.config["DATABASE"])
    dbcon.init_db(db_full_path)
    session_func = dbcon.generate_session(db_full_path)
    current_session = session_func()

    @app.route("/")
    def render_main():
        """render main page (video library + book summary)"""
        video_lib = app.config["LIB_PATH_VIDEO"]
        book_lib  = app.config["LIB_PATH_BOOK"]
        book_available = os.path.isdir(book_lib)
        books = dbcon.Book.all(current_session) if book_available else []
        book_tags = dbcon.Tag.all(current_session, target_type="book") if book_available else []
        return render_template(
            "main.html",
            actresses=dbcon.Actress.all(current_session),
            tags=dbcon.Tag.all(current_session, target_type="movie"),
            lib_url="/static/eagle_library",
            lib_path=video_lib,
            active_lib="video",
            books=books[:12],            # top page preview (latest 12)
            book_tags=book_tags,
            book_count=len(books),
            book_lib_url="/static/eagle_book_library",
            book_lib_available=book_available,
        )

    @app.route("/books")
    def render_books():
        """render book library list page"""
        available = os.path.isdir(app.config["LIB_PATH_BOOK"])
        books = dbcon.Book.all(current_session) if available else []
        tags = dbcon.Tag.all(current_session, target_type="book") if available else []
        return render_template(
            "books.html",
            books=books,
            tags=tags,
            lib_url="/static/eagle_book_library",
            lib_path=app.config["LIB_PATH_BOOK"],
            active_lib="book",
            lib_available=available,
        )

    @app.route("/viewer")
    def rend_viewer():
        """render PDF.js viewer for a book"""
        fileid = request.args.get("id", default=None, type=str)
        if not fileid:
            return "<html><body>wrong request. fileid not exists</body></html>"
        book = dbcon.Book.get_by_fileid(fileid, current_session)
        if not book:
            return "<html><body>wrong request. book not exists</body></html>"
        tags = dbcon.Tag.get_by_movie(fileid, current_session)
        pdf_url = request.url_root.rstrip("/") + url_for("stream_book", fileid=fileid)
        return render_template(
            "viewer.html",
            book=book,
            tags=tags,
            lib_url="/static/eagle_book_library",
            lib_path=app.config["LIB_PATH_BOOK"],
            pdf_url=pdf_url,
        )

    @app.route("/stream/book/<fileid>")
    def stream_book(fileid):
        """Stream book PDF file from NAS mount"""

        def _find_nfc(folder_path, name):
            if not os.path.isdir(folder_path):
                return None
            nfc_name = unicodedata.normalize("NFC", name)
            for entry in os.listdir(folder_path):
                if unicodedata.normalize("NFC", entry) == nfc_name:
                    return entry
            return None

        book = dbcon.Book.get_by_fileid(fileid, current_session)
        if not book:
            return "not found", 404

        filename = book.name + "." + book.ext  # e.g. "ずりあや.pdf"
        folder = f"{fileid}.info"
        lib_path = app.config["LIB_PATH_BOOK"]
        folder_path = os.path.join(lib_path, "images", folder)

        actual = _find_nfc(folder_path, filename)
        if actual is None:
            return "book file not found on disk", 404

        return send_from_directory(
            folder_path,
            actual,
            conditional=True,
            as_attachment=False,
            mimetype="application/pdf",
        )

    @app.route("/api/books")
    def api_books():
        """JSON list of books (for future search)"""
        books = dbcon.Book.all(current_session)
        return jsonify([
            {"id": b.id, "name": b.name, "fileid": b.fileid,
             "ext": b.ext, "page_count": b.page_count, "size": b.size}
            for b in books
        ])

    @app.route("/actress/<name>")
    def rend_actress(name):
        """render actress page"""
        actress = dbcon.Actress.get_by_name(name, current_session)
        if not actress:
            return redirect(url_for("rend_main"))
        movies = dbcon.Movie.get_by_actress(actress.actressid, current_session)
        return render_template(
            "actress.html",
            actress=actress,
            movies=movies,
            lib_url="/static/eagle_library",
            lib_path=app.config["LIB_PATH"],
        )

    @app.route("/tag/<tag>")
    def rend_tag(tag):
        """render tag page"""
        movies = dbcon.Movie.get_by_tag(tag, current_session)
        return render_template(
            "tags.html", tag=tag, movies=movies, lib_url="/static/eagle_library", lib_path=app.config["LIB_PATH"]
        )

    @app.route("/player")
    def rend_player():
        """render player page"""
        fileid = request.args.get("id", default=None, type=str)
        if not fileid:
            return "<html><body>wrong request. fileid not exists</body></html>"
        movie = dbcon.Movie.get_by_fileid(fileid, current_session)
        if not movie:
            return "<html><body>wrong request. movie not exists</body></html>"
        filepath = movie.fileid + ".info"
        filename = request.args.get("name", default=None, type=str)
        tags = dbcon.Tag.get_by_movie(fileid, current_session)
        actresses = dbcon.Actress.get_by_movie(fileid, current_session)
        stream_url = request.url_root.rstrip("/") + url_for("stream_video", fileid=fileid)
        return render_template(
            "player.html",
            fileid=fileid,
            filepath=filepath,
            filename=filename,
            actresses=actresses,
            tags=tags,
            lib_url="/static/eagle_library",
            lib_path=app.config["LIB_PATH"],
            stream_url=stream_url,
        )

    @app.route("/stream/<fileid>")
    def stream_video(fileid):
        """Stream video file from NAS mount with range request support"""

        def _find_nfc(folder_path, name):
            """Return on-disk filename matching name under NFC/NFD-insensitive compare."""
            if not os.path.isdir(folder_path):
                return None
            nfc_name = unicodedata.normalize("NFC", name)
            for entry in os.listdir(folder_path):
                if unicodedata.normalize("NFC", entry) == nfc_name:
                    return entry
            return None

        movie = dbcon.Movie.get_by_fileid(fileid, current_session)
        if not movie:
            return "not found", 404

        filename = movie.filename + ".mp4"
        folder = f"{fileid}.info"
        lib_path = app.config["LIB_PATH"]
        folder_path = os.path.join(lib_path, "images", folder)

        # filename may have NFD/NFC drift vs on-disk name — resolve via NFC compare
        actual = _find_nfc(folder_path, filename)
        if actual is None:
            return "video file not found on disk", 404

        return send_from_directory(
            folder_path,
            actual,
            conditional=True,
            as_attachment=False,
        )

    @app.route("/movie/<fileid>", methods=["POST"])
    def render_movie(fileid):
        if request.form["rating"]:
            dbup.update_star(current_session, fileid, int(request.form["rating"]))
            # get filename
            movie = dbcon.Movie.get_by_fileid(fileid, current_session)
            if not movie:
                return "<html><body>wrong request. movie not exists</body></html>"
            return redirect(url_for("rend_player", id=fileid, name=movie.filename))

    @app.route("/admin", methods=["GET", "POST"])
    def render_admin():
        if request.method == "GET":
            return render_template("admin.html", book_count=dbcon.Book.count_all(current_session))
        task = request.form["task"]
        if task == "update_db":
            thread = dbup.UpdateThread(app, current_session)
            thread.start()
            return redirect(url_for("render_admin"))
        if task == "update_books":
            book_lib = app.config["LIB_PATH_BOOK"]
            thread = threading.Thread(
                target=dbup.update_books_from_lib,
                args=(book_lib, current_session),
                daemon=True,
            )
            thread.start()
            return redirect(url_for("render_admin"))
        if task == "drop_db":
            dbup.drop_db(current_session)
            return redirect(url_for("render_main"))
        return f"""<html><body>unknown task : {request.form["task"]}</body></html>"""

    @app.route("/player/tag/add", methods=["POST"])
    def add_tag():
        """Add a tag to a movie via AJAX"""
        data = request.get_json(force=True)
        fileid = data.get("fileid")
        tag = data.get("tag")
        if not fileid or not tag:
            return jsonify(success=False, error="missing fileid or tag"), 400
        tag = tag.strip()
        if not tag:
            return jsonify(success=False, error="empty tag"), 400
        was_added = dbcon.Tag.add_for_movie(fileid, tag, current_session)
        return jsonify(success=True, added=was_added)

    @app.route("/player/tag/remove", methods=["POST"])
    def remove_tag():
        """Remove a tag from a movie via AJAX"""
        data = request.get_json(force=True)
        fileid = data.get("fileid")
        tag = data.get("tag")
        if not fileid or not tag:
            return jsonify(success=False, error="missing fileid or tag"), 400
        dbcon.Tag.remove_for_movie(fileid, tag, current_session)
        return jsonify(success=True)

    @app.route("/random")
    def jump_random():
        total_movie_count = dbcon.Movie.count_all(current_session)
        random_id = random.randint(0, total_movie_count)
        random_movie = dbcon.Movie.get_by_id(random_id, current_session)
        if random_movie is None:
            return "<html><body>can't jump random: random item is null.</body></html>"

        logging.info("player?id=%s&name=%s", random_movie.fileid, random_movie.filename)
        # <a href="../player?id={{movie.fileid}}&name={{movie.filename}}">
        return redirect(
            url_for("rend_player", id=random_movie.fileid, name=random_movie.filename)
        )

    logging.info("app generate done!")
    return app


application = create_app()
