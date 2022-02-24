from webbrowser import get
from flask import *
from perchdb import *
import subprocess

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("main.html", actresses=get_actresses(), tags=get_tags())


@app.route("/actress/<name>")
def actress(name):
    actress = get_actressdata_by_name(name)
    movies = get_movies_by_actressid(actress.actressid)
    return render_template("actress.html", actress=actress, movies=movies)


@app.route("/tag/<tag>")
def tag(tag):
    movies = get_movies_by_tag(tag)
    return render_template("tags.html", tag=tag, movies=movies)


@app.route("/player")
# http://192.168.10.110:8000/player?id=KYB&name=hogefuga
def player():
    fileid = request.args.get('id', default=None, type=str)
    filepath = fileid + ".info"
    filename = request.args.get('name', default=None, type=str)
    tags = get_tags_by_movie(fileid)
    return render_template("player.html", filepath=filepath, filename=filename, tags=tags)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000, threaded=True)
