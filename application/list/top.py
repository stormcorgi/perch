from flask import Blueprint, redirect, url_for, render_template
from perch.repository.MemRepo import MemActressRepo, MemMovieRepo

blueprint = Blueprint("top", __name__)


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


@blueprint.route("/")
def render_main():
    """render main page"""
    repoActress = MemActressRepo(actress_dicts())
    return render_template(
        "main.html",
        actresses=repoActress.list(),
        tags={}
        # tags=dbcon.Tag.all(current_session),
    )
