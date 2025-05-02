import tkinter as tk
from tkinter import scrolledtext
import requests
import webbrowser


class WebNewsLoader:
    RSS_URL = "http://slashdot.org/slashdot.rss"

    def __init__(self, root):
        self.root = root
        self.root.title("Web News Loader")
        self.root.geometry("800x600")
        self.news_items = []

        self.titles_list = tk.Listbox(root, height=10)
        self.titles_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.titles_list.bind("<<ListboxSelect>>", self.show_description)

        self.description_text = scrolledtext.ScrolledText(root, height=10, state=tk.DISABLED)
        self.description_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.link_label = tk.Label(root, text="", fg="blue", cursor="hand2")
        self.link_label.pack(pady=5)
        self.link_label.bind("<Button-1>", self.open_link)

        self.load_text()

    def parse_text(self, text: str):
        start = text.find("<item ")
        items = []
        while start != -1:
            end = text.find("</item>", start)

            title_start = text.find("<title>", start) + len("<title>")
            title_end = text.find("</title>", start)
            title = text[title_start:title_end]

            link_start = text.find("<link>", start) + len("<link>")
            link_end = text.find("</link>", start)
            link = text[link_start:link_end]

            description_start = text.find("<description>", start) + len("<description>")
            description_end = text.find("</description>", start)
            description = text[description_start:description_end]
            description = description.split("&lt;p&gt")[0]

            items.append((title, description, link))
            start = text.find("<item ", start + 7)
        return items

    def load_text(self):
        try:
            webpage = requests.get(WebNewsLoader.RSS_URL)
            content = webpage.text
        except requests.RequestException:
            self.titles_list.insert(tk.END, "Error Loading News")
            return

        self.titles_list.delete(0, tk.END)
        self.news_items.clear()

        parsed_items = self.parse_text(content)

        if not parsed_items:
            self.titles_list.insert(tk.END, "No News Available")
            return

        for title, description, link in parsed_items:
            self.titles_list.insert(tk.END, title)
            self.news_items.append((description, link))

    def show_description(self, event):
        selected_index = self.titles_list.curselection()
        if selected_index:
            index = selected_index[0]
            if index < len(self.news_items):
                description, link = self.news_items[index]

                self.description_text.config(state=tk.NORMAL)
                self.description_text.delete("1.0", tk.END)
                self.description_text.insert(tk.END, description)
                self.description_text.config(state=tk.DISABLED)

                self.link_label.config(text=link, fg="blue")
                self.link_label.link = link

                webbrowser.open(link)

    def open_link(self, event):
        webbrowser.open(self.link_label.link)


if __name__ == "__main__":
    root = tk.Tk()
    app = WebNewsLoader(root)
    root.mainloop()
