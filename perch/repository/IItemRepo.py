import abc

from perch.domain.Folder import Folder
from perch.domain.Item import Item


class IItemRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def search_by_folder(self, folder: Folder) -> list[Item]:
        """Search Item by folder"""

    @abc.abstractmethod
    def search_by_tag(self) -> list[Item]:
        """Search Item by tag"""

    @abc.abstractmethod
    def search_by_name(self) -> Item:
        """Search Item by name"""

    @abc.abstractmethod
    def search_by_id(self) -> Item:
        """Search Item by id"""

    @abc.abstractmethod
    def list(self) -> list[Item]:
        """Get list of Item"""

    @abc.abstractmethod
    def list_folders(self):
        """Get list of Folders that contain this Item"""

    @abc.abstractmethod
    def add(self) -> int:
        """Add new Item"""

    @abc.abstractmethod
    def delete(self) -> Item:
        """Delete Item"""

    @abc.abstractmethod
    def update(self) -> Item:
        """Update new Item information"""
