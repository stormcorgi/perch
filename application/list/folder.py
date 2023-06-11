from flask import Blueprint, redirect, url_for, render_template
from perch.repository.MemRepo import MemActressRepo, MemMovieRepo

blueprint = Blueprint("folder", __name__)


def actress_dicts():
    return [
        {
            "id": "KYBJABI93CWTJ",
            "name": "新垣結衣",
            "description": "",
            "children": [],
            "modificationTime": 1641991403459,
            "tags": [],
            "password": "",
            "passwordTips": "",
        },
        {
            "id": "KYBK5NZTEWDMP",
            "name": "伊織もえ",
            "description": "",
            "children": [],
            "modificationTime": 1641992866012,
            "tags": [],
            "password": "",
            "passwordTips": "",
        },
    ]


@blueprint.route("/actress/<name>")
def rend_actress(name):
    """render actress page"""
    repoActress = MemActressRepo(actress_dicts())
    repoMovie = MemMovieRepo({})
    actress = repoActress.search_by_name(name)
    if not actress:
        return redirect(url_for("rend_main"))
    movies = repoMovie.search_by_actress(actress)
    return render_template(
        "actress.html",
        actress=actress,
        movies=movies,
    )
