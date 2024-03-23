import abc
from dataclasses import asdict, dataclass


@dataclass
class Folder(metaclass=abc.ABCMeta):
    id: str
    name: str
    description: str
    children: list[str]
    modificationTime: int
    tags: list[str]
    password: str
    passwordTips: str

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return asdict(self)
