from pprint import pprint

from src.settings import _REQUIRED_FIELDS


class Book:
    def __init__(self, params: dict[str]) -> None:
        if all(f in params for f in _REQUIRED_FIELDS):
            self.from_dict(params)
        else:
            raise Exception("Add required fields to create book object")

    def match(self, pattern: dict[str]) -> bool:
        return all(v == self.__dict__.get(k) for k, v in pattern.items())

    def update(self, params: dict[str]) -> None:
        self.from_dict(params)

    def to_dict(self) -> dict[str]:
        return self.__dict__.copy()

    def from_dict(self, params: dict[str]) -> None:
        self.__dict__.update(params)

    def print(self) -> None:
        pprint(self.__dict__)

    def __str__(self) -> str:
        return f"{self.title} - {self.author}"
