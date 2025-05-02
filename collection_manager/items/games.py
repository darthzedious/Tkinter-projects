from collection_manager.items.base_item import CollectionItem


class Game(CollectionItem):
    def __init__(self, title: str, developer: str, year: int, multiplayer: bool):
        super().__init__(title, developer, year)
        self.multiplayer = multiplayer


    def to_dict(self):
        return {
            "title": self.title,
            "developer": self.author,
            "year": self.year,
            "multiplayer": self.multiplayer,
        }
