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

    def search_by_actress(self, actress: Actress) -> list[Movie]:
        return [m for m in self.list() for f in m.folders if f == actress.id]

    def search_by_tag(self, tag: str) -> list[Movie]:
        return [m for m in self.list() for t in m.tags if t == tag]

    def list(self) -> list[Movie]:
        return [Movie.from_dict(i) for i in self.data]

    def add(self, movie: dict) -> int:
        self.data.append(movie)
        return 0

    def delete(self, id: str) -> int:
        self.data = [Movie.to_dict(m) for m in self.list() if m.id != id]
        return 0

    def update(self, movie: dict) -> int:
        if movie not in self.list():
            self.add(movie)
            return 0
        else:
            self.delete(movie)
            self.add(movie)
            return 0
