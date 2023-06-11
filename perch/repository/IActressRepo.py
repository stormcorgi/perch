import abc

from perch.domain.Actress import Actress


class IActressRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list(self) -> list[Actress]:
        """Get list of Actress"""
        pass

    @abc.abstractmethod
    def add(self) -> int:
        """Add new Actress"""
        pass

    @abc.abstractmethod
    def search_by_name(self) -> Actress:
        """Search Actress by name"""
        pass

    @abc.abstractmethod
    def search_by_id(self) -> Actress:
        """Search Actress by id"""
        pass
