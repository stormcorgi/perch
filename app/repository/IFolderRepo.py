import abc

from app.domain.Folder import Folder


class IFolderRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list(self) -> list[Folder]:
        """Get list of Folders"""

    @abc.abstractmethod
    def list_item_in_folder(self):
        """Get list of Item in Folder"""

    @abc.abstractmethod
    def add(self) -> int:
        """Add new Folder"""

    @abc.abstractmethod
    def search_by_name(self) -> Folder:
        """Search Folder by name"""

    @abc.abstractmethod
    def search_by_id(self) -> Folder:
        """Search Folder by id"""
