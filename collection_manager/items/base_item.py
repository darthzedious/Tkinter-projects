from abc import ABC, abstractmethod


class CollectionItem(ABC):
    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year

    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
