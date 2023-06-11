import abc

from perch.domain.Actress import Actress
from perch.domain.Movie import Movie


class IMovieRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def search_by_actress(self, actress: Actress) -> list[Movie]:
        """Search Movie by actress"""
        pass

    @abc.abstractmethod
    def search_by_tag(self) -> list[Movie]:
        """Search Movie by tag"""
        pass

    @abc.abstractmethod
    def search_by_name(self) -> Movie:
        """Search Movie by name"""
        pass

    @abc.abstractmethod
    def search_by_id(self) -> Movie:
        """Search Movie by id"""
        pass

    @abc.abstractmethod
    def list(self) -> list[Movie]:
        """Get list of Movie"""
        pass

    @abc.abstractmethod
    def add(self) -> int:
        """Add new Movie"""
        pass

    @abc.abstractmethod
    def delete(self) -> Movie:
        """Delete Movie"""
        pass

    @abc.abstractmethod
    def update(self) -> Movie:
        """Update new Movie"""
        pass
