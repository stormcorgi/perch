""" use flask and perchdb.py """
import os
from flask import render_template, Flask, request
from perch import perchdb as db


def create_app(test_config=None):
    """Create and configure an instance of flask app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "/perch.sqlite")
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def rend_main():
        """render main page"""
        return render_template(
            "main.html",
            actresses=db.Actress.all(),
            tags=db.Tag.all()
        )

    @app.route("/actress/<name>")
    def rend_aectress(name):
        """render actress page"""
        actress = db.Actress.get_by_name(name)
        movies = db.Movie.get_by_actress(actress.actressid)
        return render_template("actress.html", actress=actress, movies=movies)

    @app.route("/tag/<tag>")
    def rend_tag(tag):
        """render tag page"""
        movies = db.Movie.get_by_tag(tag)
        return render_template("tags.html", tag=tag, movies=movies)

    @app.route("/player")
    def rend_player():
        """render player page"""
        fileid = request.args.get('id', default=None, type=str)
        filepath = fileid + ".info"
        filename = request.args.get('name', default=None, type=str)
        tags = db.Tag.get_by_movie(fileid)
        actresses = db.Actress.get_by_movie(fileid)
        return render_template(
            "player.html",
            filepath=filepath,
            filename=filename,
            actresses=actresses,
            tags=tags
        )

    return app
