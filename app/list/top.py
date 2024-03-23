from flask import Blueprint, render_template

from app.repository.MemRepo import MemFolderRepo
from app.use_cases.ActressList import actress_list_use_case

blueprint = Blueprint("top", __name__)


data_folder = [
    {
        "id": "LHL9WA8UH3NSJ",
        "name": "Norah Jones",
        "description": "Academy Award-winning actress known for her versatile performances.",
        "children": [],
        "modificationTime": 16567890,
        "tags": ["singer", "songwriter", "pianist"],
        "password": "S3cr3tP@ssw0rd",
        "passwordTips": "Remember to include special characters and numbers in your password.",
    },
]

data_item = [
    {
        "id": "LHLC3F8KFALUE",
        "name": "test",
        "size": 2878774335,
        "btime": 1683942778000,
        "mtime": 1683942814000,
        "ext": "mp4",
        "tags": [],
        "folders": ["LHL9WA8UH3NSJ"],
        "isDeleted": False,
        "url": "",
        "annotation": "",
        "modificationTime": 1683942880687,
        "duration": 7432.512,
        "height": 1080,
        "width": 1920,
        "lastModified": 1683942945589,
        "palettes": [{"color": [4, 4, 4], "ratio": 100}],
    }
]


@blueprint.route("/")
def render_main():
    """render main page"""

    actress_list = actress_list_use_case(MemFolderRepo(data_folder))
    return render_template("main.html", actresses=actress_list, tags={})
