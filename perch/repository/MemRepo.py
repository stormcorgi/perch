from typing import Optional
from perch.domain.Actress import Actress
from perch.domain.Movie import Movie
from perch.repository.IActressRepo import IActressRepo
from perch.repository.IMovieRepo import IMovieRepo


class MemActressRepo(IActressRepo):
    def __init__(self, data: list[dict]):
        self.data = data

    def list(self) -> list[Actress]:
        return [Actress.from_dict(i) for i in self.data]

    def add(self, actress: dict) -> int:
        self.data.append(actress)
        return 0

    def search_by_id(self, id: str) -> Optional[Actress]:
        for a in self.list():
            if a.id == id:
                return a
        return None

    def search_by_name(self, name: str) -> Optional[Actress]:
        for a in self.list():
            if a.name == name:
                return a
        return None


class MemMovieRepo(IMovieRepo):
    def __init__(self, data: list[dict]):
        self.data = data

    def search_by_actress_id(self) -> list[Movie]:
        return super().search_by_actress_id()

    def search_by_actress_name(self) -> list[Movie]:
        return super().search_by_actress_name()

    def list(self) -> list[Movie]:
        return [Movie.from_dict(i) for i in self.data]

    def add(self, movie: dict) -> int:
        self.data.append(movie)
        return 0

    def search_by_id(self, id: str) -> Optional[Movie]:
        for m in self.list():
            if m.id == id:
                return m
        return None

    def search_by_name(self, name: str) -> Optional[Movie]:
        for m in self.list():
            if m.name == name:
                return m
        return None
