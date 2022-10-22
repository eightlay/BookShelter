import json

_BOOKS_PATH = "./data/books.csv"
"""Path to books storage"""
_ENTITIES_PATH = "./data/entities.json"
"""Path to entities file"""
_LANGUAGE_NAME = "ENG"
"""Code of the language to use

Options: "RUS", "ENG"
"""

"""Create variables from entities"""
with open(_ENTITIES_PATH, "r") as file:
    for var, data in json.load(file).items():
        exec(f"{var} = {data}")
