import tkinter as tk
from tkinter import Listbox, ttk
import tkinter.messagebox as mg

from src.settings import _GENERAL_FIELDS, _LANGUAGES
from src.BookShelter import BookShelter


class Interface:
    def __init__(self) -> None:
        self.shelter = BookShelter()
        self.selected_bid = None
        
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
        
        self.root.bind("<Return>", self.add_to_shelter)
        
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

    def add_to_shelter(self, event: tk.Event | None = None) -> None:
        valid = self.shelter.add(self.get_fields_values(self.fields))
        if valid:
            self.clear_fields(self.fields)
            self.update_book_list()
        else:
            mg.showerror(_LANGUAGES["add_book_error_title"],
                         _LANGUAGES["add_book_error_message"])

    def get_fields_values(self, fields: dict) -> dict[str, str]:
        return {
            k: v.get()
            for k, v in fields.items()
            if v.get() != ""
        }

    def clear_fields(self, fields: dict) -> None:
        for k in fields:
            fields[k].set("")

    def update_book_list(self) -> None:
        self.book_list.delete(0, len(self.shelter.books))
        books = sorted([str(b) for b in self.shelter.books.values()])
        self.book_list.insert(0, *books)
        
    def edit_selected(self, event: tk.Event) -> None:
        bids = self.book_list.curselection()
        
        if len(bids) > 0:
            self.selected_bid = bids[0]
            self.show_selected(self.selected_bid)

    def show_selected(self, bid: int) -> None:
        book = self.shelter.books[bid].to_dict()

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

    def delete_from_shelter(self) -> None:
        bid = self.book_list.curselection()[0]
        self.shelter.remove(bid)
        self.clear_fields(self.editing_fields)
        self.update_book_list()

    def edit_book_info(self) -> None:
        if self.selected_bid:
            self.shelter.update(self.selected_bid, self.get_fields_values(self.editing_fields))
            self.clear_fields(self.editing_fields)
            self.update_book_list()

    def books_editing(self) -> None:
        self.editing_fields, add_block = self.create_field(2)
        
        save_button = ttk.Button(
            add_block, text=_LANGUAGES["edit_book"],
            command=self.edit_book_info
        )
        save_button.pack(fill='x', expand=True)
        
        delete_button = ttk.Button(
            add_block, text=_LANGUAGES["delete_book"],
            command=self.delete_from_shelter
        )
        delete_button.pack(fill='x', expand=True)
