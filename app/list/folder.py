from flask import Blueprint, redirect, render_template, url_for

from app.list.top import data_folder, data_item
from app.repository.MemRepo import MemFolderRepo, MemItemRepo

blueprint = Blueprint("folder", __name__)


@blueprint.route("/actress/<name>")
def rend_actress(name):
    """render actress page"""
    repoActress = MemFolderRepo(data_folder)
    repoMovie = MemItemRepo(data_item)
    actress = repoActress.search_by_name(name)
    if not actress:
        return redirect(url_for("rend_main"))
    movies = repoMovie.search_by_folder(actress)
    return render_template(
        "actress.html",
        actress=actress,
        movies=movies,
    )
