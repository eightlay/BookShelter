import os
import csv
from ast import literal_eval

from src.settings import _BOOKS_PATH
from src.Book import Book


class BookShelter:
    def __init__(self) -> None:
        self._load_books()
        
    def _load_books(self) -> None:
        self._books: dict[int, Book] = {}
        
        with open(os.path.join(_BOOKS_PATH), "r+") as file:
            reader = csv.reader(file)
            
            for k, v in reader:
                self._books[int(k)] = Book(literal_eval(v))
  
        self.cid = max(self._books)

    @property
    def books(self) -> dict[int, Book]:
        return self._books.copy()
    
    def next_id(self) -> int:
        self.cid += 1
        return self.cid

    def add(self, params: dict[str]) -> bool:
        try:
            book = Book(params)
            self._books[self.next_id()] = book
        except Exception as e:
            return False
        return True

    def remove(self, bid: int) -> None:
        del self._books[bid]

    def get(self, bid: int) -> Book:
        return self._books.get(bid)

    def update(self, bid: int, params: dict[str, str]) -> bool:
        if bid not in self._books:
            return False
        
        self._books[bid] = Book(params)
        return True

    def save_close(self) -> None:
        with open(os.path.join(_BOOKS_PATH), "w+") as file:
            for bid, book in self._books.items():
                file.write(f"{bid},\"{book.to_dict()}\"\n")
