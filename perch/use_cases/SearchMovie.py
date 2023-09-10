from perch.domain.Actress import Actress
from perch.repository.IItemRepo import IItemRepo


def movie_use_case_search_by_actress(repo: IItemRepo, actress: Actress):
    return repo.search_by_folder(actress)


def movie_use_case_search_by_tag(repo: IItemRepo, tag: str):
    return repo.search_by_tag(tag)
