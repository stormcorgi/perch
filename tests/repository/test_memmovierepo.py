import pytest

from perch.domain.Actress import Actress
from perch.domain.Movie import Movie
from perch.repository.MemRepo import MemMovieRepo
from perch.repository.MemRepo import MemMovieRepo


@pytest.fixture
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
        {
            "id": "KYCE05FRMZ9K4",
            "name": "長澤まさみ",
            "description": "",
            "children": [],
            "modificationTime": 1642042997127,
            "tags": [],
            "password": "",
            "passwordTips": "",
        },
        {
            "id": "KYCEOU9DRQ7KE",
            "name": "綾瀬はるか",
            "description": "",
            "children": [],
            "modificationTime": 1642044149041,
            "tags": [],
            "password": "",
            "passwordTips": "",
        },
        {
            "id": "KYCYENXIXXSNH",
            "name": "深田恭子",
            "description": "",
            "children": [],
            "modificationTime": 1642077266598,
            "tags": [],
            "password": "",
            "passwordTips": "",
        },
        {
            "id": "KYCY2H93HRZ8O",
            "name": "有村架純",
            "description": "",
            "children": [],
            "modificationTime": 1642076698077,
            "tags": [],
            "password": "",
            "passwordTips": "",
        },
    ]


@pytest.fixture
def movies_dicts():
    return [
        {
            "id": "L09HFIKE5N4O0",
            "name": "Star",
            "size": 2927362257,
            "btime": 1683656194000,
            "mtime": 1642424095000,
            "ext": "mp4",
            "tags": ["Star"],
            "folders": ["KYBJABI93CWTJ"],
            "isDeleted": "false",
            "url": "",
            "annotation": "",
            "modificationTime": 1646221201024,
            "height": 720,
            "width": 1280,
            "duration": 12141.017687,
            "palettes": [
                {"color": [104, 68, 46], "ratio": 47, "$$hashKey": "object:10487"},
                {"color": [228, 187, 175], "ratio": 12, "$$hashKey": "object:10488"},
                {"color": [167, 135, 118], "ratio": 12, "$$hashKey": "object:10489"},
                {"color": [35, 29, 30], "ratio": 11, "$$hashKey": "object:10490"},
                {"color": [161, 108, 82], "ratio": 8, "$$hashKey": "object:10491"},
                {"color": [132, 102, 89], "ratio": 4.66, "$$hashKey": "object:10492"},
                {"color": [62, 27, 15], "ratio": 0.96, "$$hashKey": "object:10493"},
                {"color": [148, 113, 109], "ratio": 0.95, "$$hashKey": "object:10494"},
            ],
            "lastModified": 1686475571000,
            "thumbnailAt": 5388.974043,
            "star": 4,
        },
        {
            "id": "LHLC3F8KFALUE",
            "name": "AAAA-012",
            "size": 2878774335,
            "btime": 1683942778000,
            "mtime": 1683942814000,
            "ext": "mp4",
            "tags": [],
            "folders": ["LHL9WA8UH3NSJ"],
            "isDeleted": "false",
            "url": "",
            "annotation": "",
            "modificationTime": 1683942880687,
            "duration": 7432.512,
            "height": 1080,
            "width": 1920,
            "lastModified": 1683942945589,
            "palettes": [{"color": [4, 4, 4], "ratio": 100}],
        },
    ]


def test_repository_list_without_parameters(movies_dicts):
    repo = MemMovieRepo(movies_dicts)
    movies = [Movie.from_dict(i) for i in movies_dicts]
    assert repo.list() == movies


def test_repository_add(movies_dicts):
    repo = MemMovieRepo([movies_dicts[0]])
    movies = [Movie.from_dict(i) for i in movies_dicts]
    repo.add(movies_dicts[1])
    assert repo.list() == movies


def test_repository_delete(movies_dicts):
    repo = MemMovieRepo(movies_dicts)
    movies = [Movie.from_dict(i) for i in movies_dicts]
    repo.delete("L09HFIKE5N4O0")
    assert repo.list()[0].to_dict() == movies[1].to_dict()
    assert len(repo.data) == 1


def test_repository_update(movies_dicts):
    repo = MemMovieRepo([movies_dicts[0]])
    movies = [Movie.from_dict(i) for i in movies_dicts]
    # update existing data
    movies_dicts[1]["url"] = "changed"
    repo.update(movies_dicts[1])
    assert repo.data != movies
    assert repo.data[1]["url"] == "changed"
    # update not existing data
    repo.delete("L09HFIKE5N4O0")
    assert len(repo.data) == 1
    repo.update(movies_dicts[1])
    assert len(repo.data) == 2


def test_repository_search_by_id(movies_dicts):
    repo = MemMovieRepo(movies_dicts)
    target = repo.search_by_id("LHLC3F8KFALUE")
    if target is not None:
        assert target.name == "AAAA-012"
    else:
        assert 1 is 2
    non_exist = repo.search_by_id("NONEXIST")
    assert non_exist is None


def test_repository_search_by_name(movies_dicts):
    repo = MemMovieRepo(movies_dicts)
    target = repo.search_by_name("AAAA-012")
    if target is not None:
        assert target.id == "LHLC3F8KFALUE"
    else:
        assert 1 is 2
    non_exist = repo.search_by_name("名無しのファイル")
    assert non_exist is None


def test_search_by_actress(movies_dicts, actress_dicts):
    repo = MemMovieRepo(movies_dicts)

    result = repo.search_by_actress(Actress.from_dict(actress_dicts[0]))
    assert result[0].id == "L09HFIKE5N4O0"


def test_search_by_tag(movies_dicts):
    repo = MemMovieRepo(movies_dicts)

    result = repo.search_by_tag("Star")
    assert result[0].id == "L09HFIKE5N4O0"
