from pprint import pprint

from src.settings import _REQUIRED_FIELDS


class Book:
    """Class to store book's info. 
    
    General and required book fields are listed in `data/entities.json`
    """
    def __init__(self, params: dict[str, str]) -> None:
        if all(f in params for f in _REQUIRED_FIELDS):
            self.from_dict(params)
        else:
            raise Exception("Add required fields to create book object")

    def match(self, pattern: dict[str, str]) -> bool:
        """Check if book matches patter

        Args:
            pattern (dict[str, str]): pattern to match with

        Returns:
            bool: does book match patter or not
        """
        return all(v == self.__dict__.get(k) for k, v in pattern.items())

    def update(self, params: dict[str, str]) -> None:
        """Update book fields with new data

        Args:
            params (dict[str, str]): new data
        """
        self.from_dict(params)

    def to_dict(self) -> dict[str, str]:
        """Book to dict

        Returns:
            dict[str, str]: book's fields
        """
        return self.__dict__.copy()

    def from_dict(self, params: dict[str, str]) -> None:
        self.__dict__.update(params)

    def print(self) -> None:
        """Print book's fields
        """
        pprint(self.__dict__)

    def __str__(self) -> str:
        return f"{self.title} - {self.author}"
