import pytest

from perch.domain.Actress import Actress
from perch.domain.Movie import Movie
from perch.repository.MemRepo import MemActressRepo
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
    ]


def test_repository_list_without_parameters(actress_dicts):
    repo = MemActressRepo(actress_dicts)
    actresses = [Actress.from_dict(i) for i in actress_dicts]
    assert repo.list() == actresses


def test_repository_add(actress_dicts):
    repo = MemActressRepo([actress_dicts[0]])
    actresses = [Actress.from_dict(i) for i in actress_dicts]
    repo.add(actress_dicts[1])
    assert repo.list() == actresses


def test_repository_search_by_id(actress_dicts):
    repo = MemActressRepo(actress_dicts)
    target = repo.search_by_id("KYBK5NZTEWDMP")
    if target is not None:
        assert target.name == "伊織もえ"
    else:
        assert 1 is 2
    non_exist = repo.search_by_id("NONEXIST")
    assert non_exist is None


def test_repository_search_by_name(actress_dicts):
    repo = MemActressRepo(actress_dicts)
    target = repo.search_by_name("伊織もえ")
    if target is not None:
        assert target.id == "KYBK5NZTEWDMP"
    else:
        assert 1 is 2
    non_exist = repo.search_by_name("名無しの権兵衛")
    assert non_exist is None
