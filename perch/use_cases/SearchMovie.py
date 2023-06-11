from perch.domain.Movie import Movie
from perch.domain.Actress import Actress
from perch.repository.IMovieRepo import IMovieRepo


def movie_use_case_search_by_actress(repo: IMovieRepo, actress: Actress):
    return repo.search_by_actress(actress)


def movie_use_case_search_by_tag(repo: IMovieRepo, tag: str):
    return repo.search_by_tag(tag)
