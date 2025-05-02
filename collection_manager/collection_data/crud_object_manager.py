import json

from collection_manager.items.books import Book
from collection_manager.items.games import Game
from collection_manager.items.movies import Movie


class CollectionManager:
    def __init__(self, filename="collection.json"):
        self.filename = filename
        self.items = {"books": [], "games": [], "movies": []}
        self.load()


    def load(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.items = {
                    "books": [Book(**item) for item in data.get("books", [])],
                    "games": [
                        Game(
                            title=item.get("title", "Unknown"),
                            developer=item.get("developer", item.get("author", "Unknown Developer")),
                            year=item.get("year",),
                            multiplayer=item.get("multiplayer", False),
                        ) for item in data.get("games", [])
                    ],
                    "movies": [Movie(**item) for item in data.get("movies", [])],
                }
        except FileNotFoundError:
            self.items = {"books": [], "games": [], "movies": []}


    def save(self):
        """
        Overwrites the data every time when called according to the current state of the collection.
        """
        data = {
            "books": [item.to_dict() for item in self.items["books"]],
            "games": [item.to_dict() for item in self.items["games"]],
            "movies": [item.to_dict() for item in self.items["movies"]],
        }

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)


    def add_item(self, category, item):
        self.items[category].append(item)
        self.save()


    def delete_item(self, category, title):
        self.items[category] = [item for item in self.items[category] if item.title != title]
        self.save()


    def edit_item(self, category, old_item, new_title=None, new_author=None, new_year=None):
        for i, item in enumerate(self.items[category]):
            if item.title == old_item.title:
                if new_title:
                    item.title = new_title
                if new_author:
                    if hasattr(item, "author"):
                        item.author = new_author
                    elif hasattr(item, "developer"):
                        item.developer = new_author
                if new_year:
                    item.year = new_year
                self.save()
                return
        raise ValueError("Item not found")


    def search(self,category, query, filter=None):
        query = query.lower()
        filtered_items = []
        filter_type = filter

        if filter_type == "All":
            for item in self.items[category]:
                filtered_items.append((item.title, item.author, item.year))
            return filtered_items

        for item in self.items[category]:
            if (
                    (filter_type == "Title" and query in item.title.lower()) or
                    (filter == "Author" and query in item.author.lower()) or
                    (filter == "Year" and str(item.year).startswith(query))
            ):
                filtered_items.append((item.title, item.author, item.year))

        return filtered_items
