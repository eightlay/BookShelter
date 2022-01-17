import tkinter as tk
from tkinter import Listbox, ttk

from src.settings import _GENERAL_FIELDS, _LANGUAGES
from src.BookShelter import BookShelter


class Interface:
    def __init__(self) -> None:
        self.shelter = BookShelter()

        self.init_root()
        self.books_adding()
        self.books_surfing()
        self.books_editing()

    def start(self) -> None:
        self.start_mainloop()

    def start_mainloop(self) -> None:
        self.root.mainloop()

    def init_root(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("720x481")
        self.root.resizable(False, False)
        self.root.title(_LANGUAGES["book_shelter"])

        def on_close():
            self.shelter.close()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_close)

    def create_field(self, col: int) -> tuple[dict[int, tk.StringVar], ttk.Frame]:
        # Store book's title and author
        fields = {k: tk.StringVar() for k in _GENERAL_FIELDS}

        # Add book frame
        block = ttk.Frame(self.root)
        block.grid(column=col, row=0, padx=10)

        # Add fields to frame
        for k, v in fields.items():
            label = ttk.Label(block, text=_LANGUAGES[k])
            label.pack(fill='y', expand=True)

            entry = ttk.Entry(block, textvariable=v, justify='center')
            entry.pack(fill='x', expand=True)

        return (fields, block)

    def books_adding(self) -> None:
        self.fields, add_block = self.create_field(0)
        
        login_button = ttk.Button(
            add_block, text=_LANGUAGES["add_book"],
            command=self.add_to_shelter
        )
        login_button.pack(pady=10, fill='x', expand=True)

    def add_to_shelter(self) -> None:
        self.shelter.add(self.get_fields_values())
        self.clear_fields()
        self.update_book_list()

    def get_fields_values(self) -> dict[str, str]:
        return {
            k: v.get()
            for k, v in self.fields.items()
            if v.get() != ""
        }

    def clear_fields(self) -> None:
        for k in self.fields:
            self.fields[k].set("")

    def update_book_list(self) -> None:
        self.book_list.delete(0, len(self.shelter.books))
        self.book_list.insert(0, *self.shelter.books.values())

    def edit_selected(self, event: tk.Event) -> None:
        bid = self.book_list.curselection()
        self.show_selected(bid)

    def show_selected(self, bids: int) -> None:
        book = self.shelter.books[bids[0]].to_dict()

        for field in _GENERAL_FIELDS:
            self.editing_fields[field].set(book.get(field, ""))

    def books_surfing(self) -> None:
        surf_books = ttk.Frame(self.root)
        surf_books.grid(column=1, row=0, padx=10)

        self.book_list = Listbox(surf_books, width=30,
                                 height=27, justify='center')
        self.book_list.pack(pady=10)
        self.book_list.bind("<<ListboxSelect>>", self.edit_selected)

        self.update_book_list()
        
    def books_editing(self) -> None:
        self.editing_fields, add_block = self.create_field(2)
        
        login_button = ttk.Button(
            add_block, text=_LANGUAGES["add_book"],
            command=self.add_to_shelter
        )
        login_button.pack(pady=10, fill='x', expand=True)
