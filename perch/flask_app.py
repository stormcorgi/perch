""" use flask and perchdb.py """
import datetime
import logging
import os
import random

import perch.db.connection as dbcon
import perch.db.update as dbup
from flask import Flask, redirect, render_template, request, url_for

start_dt = datetime.datetime.now()
start_str = start_dt.strftime("%Y%m%d-%H")
logging.basicConfig(
    level=logging.INFO,
    filename=f"./log/perch-{start_str}.log",
    format="%(asctime)s %(message)s",
)


def create_app():
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
    def rend_main():
        """render main page"""
        return render_template(
            "main.html",
            actresses=dbcon.Actress.all(current_session),
            tags=dbcon.Tag.all(current_session),
            lib_path=app.config["LIB_PATH"],
        )

    @app.route("/actress/<name>")
    def rend_aectress(name):
        """render actress page"""
        actress = dbcon.Actress.get_by_name(name, current_session)
        movies = dbcon.Movie.get_by_actress(actress.actressid, current_session)
        return render_template(
            "actress.html",
            actress=actress,
            movies=movies,
            lib_path=app.config["LIB_PATH"],
        )

    @app.route("/tag/<tag>")
    def rend_tag(tag):
        """render tag page"""
        movies = dbcon.Movie.get_by_tag(tag, current_session)
        return render_template(
            "tags.html", tag=tag, movies=movies, lib_path=app.config["LIB_PATH"]
        )

    @app.route("/player")
    def rend_player():
        """render player page"""
        fileid = request.args.get("id", default=None, type=str)
        filepath = fileid + ".info"
        filename = request.args.get("name", default=None, type=str)
        tags = dbcon.Tag.get_by_movie(fileid, current_session)
        actresses = dbcon.Actress.get_by_movie(fileid, current_session)
        return render_template(
            "player.html",
            filepath=filepath,
            filename=filename,
            actresses=actresses,
            tags=tags,
            lib_path=app.config["LIB_PATH"],
        )

    @app.route("/admin", methods=["GET", "POST"])
    def render_admin():
        if request.method == "GET":
            return render_template("admin.html")
        # POST section
        if request.form["task"] == "update_db":
            thread = dbup.UpdateThread(app, current_session)
            thread.start()
            return """<html><body>request queued.</body></html>"""

        if request.form["task"] == "drop_db":
            dbup.drop_db(current_session)
            return f"""<html><body>{request.form["task"]} done!</body></html>"""

        return f"""<html><body>unknown task : {request.form["task"]}</body></html>"""

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
