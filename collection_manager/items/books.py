from collection_manager.items.base_item import CollectionItem


class Book(CollectionItem):
    def __init__(self, title: str, author: str, year: int, genre: str, pages: int):
        super().__init__(title, author, year)
        self.genre = genre
        self.pages = pages

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "pages": self.pages,
        }
