import abc
from dataclasses import asdict, dataclass


@dataclass
class Item(metaclass=abc.ABCMeta):
    id: str
    name: str
    size: int
    btime: int
    mtime: int
    ext: str
    tags: list[str]
    folders: list[str]
    isDeleted: bool
    url: str
    annotation: str
    modificationTime: int
    duration: float
    height: int
    width: int
    lastModified: int
    palettes: list[dict]
    star: int = 0
    thumbnailAt: float = 0.0

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return asdict(self)
