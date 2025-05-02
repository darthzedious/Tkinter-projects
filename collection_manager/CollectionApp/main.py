import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from collection_manager.collection_data.crud_object_manager import CollectionManager
from collection_manager.items.books import Book
from collection_manager.items.games import Game
from collection_manager.items.movies import Movie


class CollectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Collection Manager App")
        self.root.geometry("830x450")
        self.root.resizable(False, False)
        self.manager = CollectionManager()

        #main frame
        self.main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.main_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        #a frame where the categories are displayed
        self.category_frame = ttk.Frame(self.main_frame,)
        self.category_frame.grid(column=4, row=0, columnspan=3, pady=50, padx=240, sticky="nsew")

        self.category_tree = ttk.Treeview(self.category_frame, columns=("Category"), show="headings", height=12)
        self.category_tree.heading("Category", text="Category")
        self.category_tree.column("Category", width=300, anchor="center")
        self.category_tree.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        #details button to redirect to selected collection
        self.details_button = ttk.Button(self.category_frame, text="Details", command=self.show_category)
        self.details_button.grid(column=0, row=1, pady=5)

        for category in self.manager.items.keys():
            self.category_tree.insert("", tk.END, values=(category,))

        #collection items frame
        self.item_frame = ttk.Frame(self.main_frame)
        self.tree = ttk.Treeview(self.item_frame, columns=("Title", "Author", "Year"), show="headings", height=12)
        for col in ("Title", "Author", "Year"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=220, anchor="center")
        self.tree.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")

        #search frame
        self.search_frame = ttk.Frame(self.item_frame)
        self.search_frame.grid(row=0, column=0, columnspan=3, pady=10)

        #seach entry, button, filter
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=51)
        self.search_entry.grid(column=1, row=0, padx=5)
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search)
        self.search_button.grid(column=2, row=0, padx=5)

        self.search_filter = tk.StringVar(value="All")
        self.search_filter_menu = ttk.Combobox(self.search_frame, textvariable=self.search_filter, state="readonly",
                                               values=["All", "Title", "Author", "Year"])
        self.search_filter_menu.grid(column=0, row=0, padx=5)

        #CRUD buttons frame
        self.button_frame = ttk.Frame(self.item_frame)
        self.button_frame.grid(column=0, row=3, pady=10)

        ttk.Button(self.button_frame, text="Add Item", command=self.add_item).grid(column=0, row=0, padx=5)
        ttk.Button(self.button_frame, text="Edit Item", command=self.edit_item).grid(column=1, row=0, padx=5)
        ttk.Button(self.button_frame, text="Delete Item", command=self.delete_item).grid(column=2, row=0, padx=5)
        ttk.Button(self.button_frame, text="Back", command=self.show_categories).grid(column=3, row=0, padx=5)


    def show_category(self):
        selected = self.category_tree.selection()
        if not selected:
            messagebox.showerror(title="Error", message="No category selected!")
            return

        self.selected_category = self.category_tree.item(selected[0])["values"][0]
        self.category_frame.grid_forget()
        self.item_frame.grid(column=0, row=1, columnspan=3, pady=10, sticky="nsew")
        self.refresh()


    def show_categories(self):
        self.item_frame.grid_forget()
        self.category_frame.grid(column=4, row=0, columnspan=3, pady=50, padx=240, sticky="nsew")


    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.manager.items[self.selected_category]:
            self.tree.insert("", tk.END, values=(item.title, item.author, item.year))


    def add_item(self):
        category = self.selected_category
        if category not in self.manager.items:
            messagebox.showerror(title="Error", message="No item selected!")
            return

        objects = {
            "books": Book,
            "games": Game,
            "movies": Movie
        }

        item_class = objects.get(category)
        if not item_class:
            messagebox.showerror(title="Error", message="Unknown category!")
            return

        attributes = self.collect_item_attributes(item_class)
        item = item_class(**attributes)

        self.manager.add_item(category, item)
        self.refresh()


    def collect_item_attributes(self, item):
        """
        This method will collect the attributes of the item in a dictionary and
        create a way for the user to assign the desired data correctly.
        The method accepts item which is the class of the object that will be created later on.

        :return: dict with the attributes of the item as keys and a dialog window that asks
        for the data to be set as value.
        """
        attributes = {}

        for attribute in item.__init__.__code__.co_varnames[1:]: # makes tuple of all attributes of the item class without the self
            # annotations is a dict with attr from the init as key and type as value
            attribute_type = item.__annotations__.get(attribute, str) # gets the type for the attr , if error set as str

            if attribute_type == int:
                dialog = simpledialog.askinteger(attribute.capitalize(), f"Enter {attribute}:")
            elif attribute_type == float:
                dialog = simpledialog.askfloat(attribute.capitlize(), f"Enter {attribute}:")
            else:
                dialog = simpledialog.askstring(attribute.capitalize(), f"Enter {attribute}:")

            if dialog is None:
                raise ValueError("User cancelled the input")

            attributes[attribute] = dialog

        return attributes


    def delete_item(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            title = item["values"][0]
            self.manager.delete_item(self.selected_category, title)
            self.refresh()
        else:
            messagebox.showerror(title="Error", message="No item selected!")


    def edit_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror(title="Error", message="No item selected!")
            return

        item = self.tree.item(selected[0])
        title = item["values"][0]

        for item in self.manager.items[self.selected_category]:
            if item.title == title:
                break
        else:
            messagebox.showerror(title="Error", message="Item not found!")
            return

        new_title = simpledialog.askstring(title=f"Edit Title:", prompt="Enter new title:", initialvalue=item.title)
        new_author = simpledialog.askstring(title=f"Edit Creator:", prompt="Enter new creator:", initialvalue=item.author)
        new_year = simpledialog.askinteger(title=f"Edit Year:", prompt="Enter new year:", initialvalue=item.year)

        self.manager.edit_item(
            self.selected_category,
            item,
            new_title=new_title if new_author else item.title,
            new_author=new_author if new_author else item.author if hasattr(item, "author") else item.author,
            new_year=new_year if new_author else item.year
        )
        self.refresh()


    def search(self):
        query = self.search_var.get()
        filter = self.search_filter.get()
        if not query:
            return

        filtered_items = self.manager.search(self.selected_category,query, filter)

        self.tree.delete(*self.tree.get_children())
        for entry in filtered_items:
            self.tree.insert("", tk.END, values=entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = CollectionApp(root)
    root.mainloop()
