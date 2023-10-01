""" use flask and perchdb.py """
from flask import render_template, Flask, request
from perchdb import Actress, Movie, Tag

app = Flask(__name__)


@app.route("/")
def rend_main():
    """render main page"""
    return render_template(
        "main.html",
        actresses=Actress.all(),
        tags=Tag.all()
    )


@app.route("/actress/<name>")
def rend_aectress(name):
    """render actress page"""
    actress = Actress.get_by_name(name)
    movies = Movie.get_by_actress(actress.actressid)
    return render_template("actress.html", actress=actress, movies=movies)


@app.route("/tag/<tag>")
def rend_tag(tag):
    """render tag page"""
    movies = Movie.get_by_tag(tag)
    return render_template("tags.html", tag=tag, movies=movies)


@app.route("/player")
def rend_player():
    """render player page"""
    fileid = request.args.get('id', default=None, type=str)
    filepath = fileid + ".info"
    filename = request.args.get('name', default=None, type=str)
    tags = Tag.get_by_movie(fileid)
    actresses = Actress.get_by_movie(fileid)
    return render_template(
        "player.html",
        filepath=filepath,
        filename=filename,
        actresses=actresses,
        tags=tags
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9000, threaded=True)
