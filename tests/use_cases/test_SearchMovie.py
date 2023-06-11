from unittest import mock
import pytest

from perch.domain.Actress import Actress
from perch.domain.Movie import Movie
from perch.repository.MemRepo import MemMovieRepo
from perch.use_cases.SearchMovie import movie_use_case_search_by_actress


@pytest.fixture
def domain_actresses():
    actress_1 = Actress(
        id="ASDFVZSC",
        name="Norah Jones",
        description="Academy Award-winning actress known for her versatile performances.",
        children=[],
        modificationTime=16567890,
        tags=["singer", "songwriter", "pianist"],
        password="S3cr3tP@ssw0rd",
        passwordTips="Remember to include special characters and numbers in your password.",
    )

    actress_2 = Actress(
        id="QWERTYUI",
        name="Scarlett Johansson",
        description="Renowned actress and one of the highest-paid actresses in the world.",
        children=[],
        modificationTime=19876543,
        tags=["Marvel", "Black Widow", "Avengers"],
        password="SecurePass123",
        passwordTips="Choose a password with a combination of uppercase and lowercase letters.",
    )

    actress_3 = Actress(
        id="ZXCVBNMQ",
        name="Meryl Streep",
        description="Legendary actress with a record-setting number of Academy Award nominations.",
        children=[],
        modificationTime=12233445,
        tags=["Drama", "Hollywood", "Icon"],
        password="M3rylStr33p!",
        passwordTips="Avoid using common words as your password.",
    )

    actress_4 = Actress(
        id="LKJHGFDS",
        name="Jennifer Lawrence",
        description="Talented actress known for her down-to-earth personality and relatable roles.",
        children=[],
        modificationTime=14567890,
        tags=["The Hunger Games", "X-Men", "Oscar Winner"],
        password="JL@wrenc3P@ss",
        passwordTips="Include a mix of letters, numbers, and symbols in your password.",
    )

    actress_5 = Actress(
        id="POIUYTRE",
        name="Emma Stone",
        description="Academy Award-winning actress recognized for her charismatic performances.",
        children=[],
        modificationTime=17765432,
        tags=["La La Land", "Easy A", "Comedy"],
        password="EStone@123",
        passwordTips="Change your password regularly to maintain security.",
    )
    return [actress_1, actress_2, actress_3, actress_4, actress_5]


@pytest.fixture
def domain_movies():
    return [
        {
            "id": "L09HFIKE5N4O0",
            "name": "Star",
            "size": 2927362257,
            "btime": 1683656194000,
            "mtime": 1642424095000,
            "ext": "mp4",
            "tags": ["star"],
            "folders": ["POIUYTRE"],
            "isDeleted": "false",
            "url": "",
            "annotation": "",
            "modificationTime": 1646221201024,
            "height": 720,
            "width": 1280,
            "duration": 12141.017687,
            "palettes": [
                {"color": [250, 247, 240], "ratio": 36, "$$hashKey": "object:6548"},
                {"color": [202, 170, 136], "ratio": 26, "$$hashKey": "object:6549"},
                {"color": [169, 135, 106], "ratio": 10, "$$hashKey": "object:6550"},
                {"color": [242, 213, 180], "ratio": 6, "$$hashKey": "object:6551"},
                {"color": [87, 60, 43], "ratio": 5, "$$hashKey": "object:6552"},
                {"color": [134, 93, 66], "ratio": 4.69, "$$hashKey": "object:6553"},
                {"color": [218, 191, 171], "ratio": 4.35, "$$hashKey": "object:6554"},
                {"color": [171, 157, 132], "ratio": 3, "$$hashKey": "object:6555"},
                {"color": [166, 142, 128], "ratio": 2.01, "$$hashKey": "object:6556"},
                {"color": [125, 97, 90], "ratio": 0.45, "$$hashKey": "object:6557"},
            ],
            "lastModified": 1686475467000,
            "thumbnailAt": 5388.974043,
            "star": 4,
        }
    ]


def test_movie_use_case_search_by_actress(domain_movies, domain_actresses):
    repo = MemMovieRepo(domain_movies)

    result = movie_use_case_search_by_actress(repo, domain_actresses[-1])
    assert result[0].to_dict() == domain_movies[0]
