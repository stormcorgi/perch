from flask import Blueprint, render_template, request, current_app
from perch.repository.MemRepo import MemItemRepo
from application.list.top import data_item

blueprint = Blueprint("item", __name__)


@blueprint.route("/player")
def rend_player():
    """render player page"""

    fileid = request.args.get("id", default=None, type=str)
    if fileid is None:
        return "fileid is none."
    repoMovie = MemItemRepo(data_item)
    movie = repoMovie.search_by_id(fileid)
    if movie is None:
        return "no movie here."
    # filepath = movie.id + ".info"
    # filename = request.args.get("name", default=None, type=str) + movie.ext
    actresses = repoMovie.list_folders(movie)
    if movie.star is None:
        movie.star = 0
    return render_template(
        "player.html",
        movie=movie,
        actresses=actresses,
        lib_path=current_app.config.get("LIB_PATH"),
    )


@blueprint.route("/viewer")
def rend_viewer():
    """render viewer page"""
    return "WIP"
    # fileid = request.args.get("id", default=None, type=str)
    # if fileid is None:
    #     return "fileid is none."
    # repoMovie = MemItemRepo(data_item)
    # movie = repoMovie.search_by_id(fileid)
    # if movie is None:
    #     return "no movie here."
    # # filepath = movie.id + ".info"
    # # filename = request.args.get("name", default=None, type=str) + movie.ext
    # actresses = repoMovie.list_folders(movie)
    # if movie.star is None:
    #     movie.star = 0
    # return render_template(
    #     "player.html",
    #     fileid=fileid,
    #     filepath=filepath,
    #     filename=filename,
    #     actresses=actresses,
    #     lib_path=current_app.config.get("LIB_PATH"),
    #     star=movie.star,
    # )
