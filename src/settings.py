import json

_BOOKS_PATH = "./data/books.csv"
_ENTITIES_PATH = "./data/entities.json"
_LANGUAGE_NAME = "RUS"


with open(_ENTITIES_PATH, "r") as file:
    for var, data in json.load(file).items():
        exec(f"{var} = {data}")
