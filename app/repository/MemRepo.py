from typing import Optional

from app.domain.Folder import Folder
from app.domain.Item import Item
from app.repository.IFolderRepo import IFolderRepo
from app.repository.IItemRepo import IItemRepo


class MemFolderRepo(IFolderRepo):
    def __init__(self, data: list[dict]):
        self.data = data

    def list(self) -> list[Folder]:
        return [Folder.from_dict(i) for i in self.data]

    def list_item_in_folder(self, folder: Folder):
        return MemItemRepo(self.data).search_by_folder(folder)

    def add(self, folder: dict) -> int:
        self.data.append(folder)
        return 0

    def search_by_id(self, id: str) -> Optional[Folder]:
        for folder in self.list():
            if folder.id == id:
                return folder
        return None

    def search_by_name(self, name: str) -> Optional[Folder]:
        for folder in self.list():
            if folder.name == name:
                return folder
        return None


class MemItemRepo(IItemRepo):
    def __init__(self, data: list[dict]):
        self.data = data

    def search_by_id(self, id: str) -> Optional[Item]:
        for item in self.list():
            if item.id == id:
                return item
        return None

    def search_by_name(self, name: str) -> Optional[Item]:
        for item in self.list():
            if item.id == name:
                return item
        return None

    def search_by_folder(self, folder: Folder) -> list[Item]:
        return [i for i in self.list() for f in i.folders if f == folder.id]

    def search_by_tag(self, tag: str) -> list[Item]:
        return [i for i in self.list() for t in i.tags if t == tag]

    def list(self) -> list[Item]:
        return [Item.from_dict(i) for i in self.data]

    def list_folders(self, item: Item):
        return item.folders

    def add(self, item: dict) -> int:
        self.data.append(item)
        return 0

    def delete(self, id: str) -> int:
        self.data = [Item.to_dict(i) for i in self.list() if i.id != id]
        return 0

    def update(self, item: dict) -> int:
        try:
            if item not in self.list():
                self.add(item)
                return 0
            else:
                self.delete(item)
                self.add(item)
                return 0
        except:
            return 1
