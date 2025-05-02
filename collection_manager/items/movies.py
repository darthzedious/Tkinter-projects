from collection_manager.items.base_item import CollectionItem


class Movie(CollectionItem):
    def __init__(self, title: str, director: str, year: int, rating: float):
        super().__init__(title, director, year)
        self.rating = rating

    def to_dict(self):
        return {
            "title": self.title,
            "director": self.author,
            "year": self.year,
            "rating": self.rating,
        }
