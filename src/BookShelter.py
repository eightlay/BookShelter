import os
import csv
from ast import literal_eval

from src.settings import _BOOKS_PATH
from src.Book import Book


class BookShelter:
    def __init__(self) -> None:
        self._load_books()
        
    def _load_books(self) -> None:
        self._books = {}
        
        with open(os.path.join(_BOOKS_PATH), "r+") as file:
            reader = csv.reader(file)
            for k, v in reader:
                self._books[int(k)] = Book(literal_eval(v))
  
        self.cid = max(self._books)

    @property
    def books(self) -> dict[int, Book]:
        return self._books
    
    def next_id(self) -> int:
        self.cid += 1
        return self.cid

    def add(self, params: dict[str]) -> bool:
        try:
            book = Book(params)
            self._books[self.next_id()] = book
            
            # with open(os.path.join(_BOOKS_PATH), "a") as file:
            #     file.write(f"\n{self.cid},\"{book.to_dict()}\"")
        except Exception as e:
            return False
        return True

    def remove(self, bid: int) -> None:
        del self._books[bid]

    def get(self, bid: int) -> Book:
        return self._books.get(bid)

    def update(self, bid: int, params: dict[str]) -> None:
        if bid in self._books:
            self._books[bid] = Book(params)
        else:
            raise Exception(f"There is no book with id {bid}")

    def close(self) -> None:
        with open(os.path.join(_BOOKS_PATH), "w+") as file:
            for bid, book in self._books.items():
                file.write(f"{bid},\"{book.to_dict()}\"\n")