import abc

from perch.domain.Movie import Movie


class IMovieRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def search_by_actress_id(self) -> list[Movie]:
        """Search Movie by actress id"""
        pass

    @abc.abstractmethod
    def search_by_actress_name(self) -> list[Movie]:
        """Search Movie by actress name"""
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
    def search_by_name(self) -> Movie:
        """Search Movie by name"""
        pass

    @abc.abstractmethod
    def search_by_id(self) -> Movie:
        """Search Movie by id"""
        pass
