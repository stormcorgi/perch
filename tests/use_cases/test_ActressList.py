from unittest import mock
import pytest

from perch.domain.Actress import Actress
from perch.use_cases.ActressList import actress_list_use_case


@pytest.fixture
def domain_acresses():
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


def test_actress_list_without_parameters(domain_acresses):
    repo = mock.Mock()
    repo.list.return_value = domain_acresses

    result = actress_list_use_case(repo)
    repo.list.assert_called_with()
    assert result == domain_acresses
