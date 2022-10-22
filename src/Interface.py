import tkinter as tk
from tkinter import Listbox, ttk
import tkinter.messagebox as mg

from src.Book import Book
from src.BookShelter import BookShelter
from src.settings import _GENERAL_FIELDS, _LANGUAGES, _LANGUAGE_NAME

FIELD_NAMES = _LANGUAGES[_LANGUAGE_NAME]


class Interface:
    def __init__(self) -> None:
        self.shelter = BookShelter()
        self.selected_bid = None
        
        self.init_root()
        self.books_adding()
        self.books_surfing()
        self.books_editing()

    def start(self) -> None:
        """Start app
        """
        self.root.mainloop()

    def init_root(self) -> None:
        """Init Tkinter
        """
        self.root = tk.Tk()
        self.root.geometry("720x481")
        self.root.resizable(False, False)
        self.root.title(FIELD_NAMES["book_shelter"])
        
        self.root.bind("<Return>", self.add_to_shelter)
        
        def on_close():
            self.shelter.save()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_close)

    def create_field(self, col: int) -> tuple[dict[str, tk.StringVar], ttk.Frame]:
        """Create field block

        Args:
            col (int): number of columns in the block

        Returns:
            tuple[dict[str, tk.StringVar], ttk.Frame]: fields and block
        """
        # Store book's info
        fields = {k: tk.StringVar() for k in _GENERAL_FIELDS}

        # Add book frame
        block = ttk.Frame(self.root)
        block.grid(column=col, row=0, padx=10)

        # Add fields to frame
        for k, v in fields.items():
            label = ttk.Label(block, text=FIELD_NAMES[k])
            label.pack(fill='y', expand=True)

            entry = ttk.Entry(block, textvariable=v, justify='center')
            entry.pack(fill='x', expand=True)

        return (fields, block)

    def books_adding(self) -> None:
        """Create lock for book adding
        """
        self.fields, add_block = self.create_field(0)

        login_button = ttk.Button(
            add_block, text=FIELD_NAMES["add_book"],
            command=self.add_to_shelter
        )
        login_button.pack(pady=10, fill='x', expand=True)

    def add_to_shelter(self, event: tk.Event | None = None) -> None:
        """Add to shelter button creation

        Args:
            event (tk.Event | None, optional): tkinter event. Defaults to None.
        """
        valid = self.shelter.add(self.get_fields_values(self.fields))
        if valid:
            self.clear_fields(self.fields)
            self.update_book_list()
        else:
            mg.showerror(FIELD_NAMES["add_book_error_title"],
                         FIELD_NAMES["add_book_error_message"])

    def get_fields_values(self, fields: dict[str, tk.StringVar]) -> dict[str, str]:
        """Get non empty fields' values

        Args:
            fields (dict[str, str]): fields to gather data from

        Returns:
            dict[str, str]
        """
        return {
            k: v.get()
            for k, v in fields.items()
            if v.get() != ""
        }

    def clear_fields(self, fields: dict[str, tk.StringVar]) -> None:
        """Clear all the given fields

        Args:
            fields (dict[str, tk.StringVar]): fields to clear
        """
        for k in fields:
            fields[k].set("")

    def update_book_list(self) -> None:
        """Update rendered book list
        """
        self.book_list.delete(0, len(self.shelter.books))
        books = sorted([str(b) for b in self.shelter.books.values()])
        self.book_list.insert(0, *books)
        
    def edit_selected(self, event: tk.Event) -> None:
        """Show the selected book

        Args:
            event (tk.Event): tkinter event
        """
        if len(self.book_list.curselection()) > 0:
            self.selected_bid = self.get_selected_book_id()
            self.show_selected()

    def show_selected(self) -> None:
        """Show the selected book info
        """
        book = self.shelter.books[self.selected_bid].to_dict()

        for field in _GENERAL_FIELDS:
            self.editing_fields[field].set(book.get(field, ""))
        
    def get_selected_book_id(self) -> int:
        """Get currently selected book id"""
        titleAuthor = self.book_list.get(tk.ANCHOR)
        pattern = Book.split_str_repr(titleAuthor)
        return self.shelter.find_id_by_pattern(pattern)

    def books_surfing(self) -> None:
        """Book surfing section creation
        """
        surf_books = ttk.Frame(self.root)
        surf_books.grid(column=1, row=0, padx=10)

        self.book_list = Listbox(
            surf_books, width=30, height=27, justify='center'
        )
        self.book_list.pack(pady=10)
        self.book_list.bind("<<ListboxSelect>>", self.edit_selected)

        self.update_book_list()

    def delete_from_shelter(self) -> None:
        """Delete the selected book from database
        """
        bid = self.get_selected_book_id()
        
        if bid is None:
            raise IndexError("invalid book selected")
        
        self.shelter.remove(bid)
        self.clear_fields(self.editing_fields)
        self.update_book_list()

    def edit_book_info(self) -> None:
        """Edit book's info
        """
        if self.selected_bid:
            self.shelter.update(
                self.selected_bid, self.get_fields_values(self.editing_fields)
            )
            self.clear_fields(self.editing_fields)
            self.update_book_list()

    def books_editing(self) -> None:
        """Book editing section creation
        """
        self.editing_fields, add_block = self.create_field(2)
        
        save_button = ttk.Button(
            add_block, text=FIELD_NAMES["edit_book"],
            command=self.edit_book_info
        )
        save_button.pack(fill='x', expand=True)
        
        delete_button = ttk.Button(
            add_block, text=FIELD_NAMES["delete_book"],
            command=self.delete_from_shelter
        )
        delete_button.pack(fill='x', expand=True)
