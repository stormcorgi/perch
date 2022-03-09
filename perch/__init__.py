""" use flask and perchdb.py """
import os
import random
from flask import render_template, Flask, request, redirect, url_for
from perch import perchdb as db


def create_app(test_config=None):
    """Create and configure an instance of flask app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(
            app.instance_path, "perch.sqlite"),
        LIB_PATH=os.path.join(
            app.instance_path, "../perch/static/eagle_library")
    )

    if test_config is not None:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db_full_path = os.path.join(app.instance_path, app.config["DATABASE"])
    db.init_db(db_full_path)
    session_func = db.generate_session(db_full_path)
    current_session = session_func()

    @app.route("/")
    def rend_main():
        """render main page"""
        return render_template(
            "main.html",
            actresses=db.Actress.all(current_session),
            tags=db.Tag.all(current_session)
        )

    @app.route("/actress/<name>")
    def rend_aectress(name):
        """render actress page"""
        actress = db.Actress.get_by_name(name, current_session)
        movies = db.Movie.get_by_actress(actress.actressid, current_session)
        return render_template("actress.html", actress=actress, movies=movies)

    @app.route("/tag/<tag>")
    def rend_tag(tag):
        """render tag page"""
        movies = db.Movie.get_by_tag(tag, current_session)
        return render_template("tags.html", tag=tag, movies=movies)

    @app.route("/player")
    def rend_player():
        """render player page"""
        fileid = request.args.get('id', default=None, type=str)
        filepath = fileid + ".info"
        filename = request.args.get('name', default=None, type=str)
        tags = db.Tag.get_by_movie(fileid, current_session)
        actresses = db.Actress.get_by_movie(fileid, current_session)
        return render_template(
            "player.html",
            filepath=filepath,
            filename=filename,
            actresses=actresses,
            tags=tags
        )

    @app.route("/admin", methods=["GET", "POST"])
    def render_admin():
        if request.method == "GET":
            return render_template("admin.html")
        # POST section
        if request.form["task"] == "update_db":
            db.update_actress(current_session)
            db.update_files(current_session)
            db.update_count(current_session)
            return f"""<html><body>{request.form["task"]} done!</body></html>"""

        if request.form["task"] == "drop_db":
            db.drop_db(current_session)
            return f"""<html><body>{request.form["task"]} done!</body></html>"""

        return f"""<html><body>unknown task : {request.form["task"]}</body></html>"""

    @app.route("/random")
    def jump_random():
        total_movie_count = db.Movie.count_all(current_session)
        random_id = random.randint(0, total_movie_count)
        random_movie = db.Movie.get_by_id(random_id, current_session)
        print(f"player?id={random_movie.fileid}&name={random_movie.filename}")
        # <a href="../player?id={{movie.fileid}}&name={{movie.filename}}">
        return redirect(url_for("rend_player", id=random_movie.fileid, name=random_movie.filename))

    return app
