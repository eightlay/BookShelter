import os
import csv
from ast import literal_eval

from src.settings import _BOOKS_PATH
from src.Book import Book


class BookShelter:
    """Record keeping class for personal library
    """
    def __init__(self) -> None:
        self._load_books()
        
    def _load_books(self) -> None:
        """Load books from `data/books.csv` file
        """
        self._books: dict[int, Book] = {}
        
        with open(os.path.join(_BOOKS_PATH), "r+") as file:
            reader = csv.reader(file)
            
            for k, v in reader:
                self._books[int(k)] = Book(literal_eval(v))
  
        self.cid = max(self._books)

    @property
    def books(self) -> dict[int, Book]:
        """Get tracked books

        Returns:
            dict[int, Book]: tracked books
        """
        return self._books.copy()
    
    def next_id(self) -> int:
        """Generate next book id and return it

        Returns:
            int: new book id
        """
        self.cid += 1
        return self.cid

    def add(self, params: dict[str]) -> bool:
        """Add book to library

        Args:
            params (dict[str]): new book's params

        Returns:
            bool: new book successfully added
        """
        try:
            book = Book(params)
            self._books[self.next_id()] = book
        except Exception as e:
            return False
        return True

    def remove(self, bid: int) -> None:
        """Remove book from the library by its id

        Args:
            bid (int): book id
        """
        del self._books[bid]

    def get(self, bid: int) -> Book:
        """Get book by its id

        Args:
            bid (int): book id

        Returns:
            Book
        """
        return self._books.get(bid)

    def update(self, bid: int, params: dict[str, str]) -> bool:
        """Update tracked book info

        Args:
            bid (int): book id
            params (dict[str, str]): new info

        Returns:
            bool: successfully updated
        """
        if bid not in self._books:
            return False
        
        self._books[bid] = Book(params)
        return True

    def save_close(self) -> None:
        """Write data to `data/books.csv`
        """
        with open(os.path.join(_BOOKS_PATH), "w+") as file:
            for bid, book in self._books.items():
                file.write(f"{bid},\"{book.to_dict()}\"\n")
