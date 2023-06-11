from perch.domain.Actress import Actress
from perch.repository.IActressRepo import IActressRepo


def actress_list_use_case(repo: IActressRepo) -> list[Actress]:
    return repo.list()
