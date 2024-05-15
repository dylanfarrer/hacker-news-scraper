from tkinter import *
from tkinter import ttk
import webbrowser
import requests
from bs4 import BeautifulSoup


def fetch_news():
    print("Fetching news...")
    try:
        res = requests.get("https://news.ycombinator.com/news")
        res.raise_for_status()
        print("Successfully fetched HTML content.")

        soup = BeautifulSoup(res.text, "html.parser")
        prelinks = soup.select(".titleline a")

        links = [link.get("href") for link in prelinks]
        subtext = [subtext.text for subtext in prelinks]

        # Remove every other link
        links = links[::2]
        subtext = subtext[::2]

        print(links[:5])
        print(subtext[:5])

        print(len(links))
        print(len(subtext))

        if len(links) != len(subtext):
            raise Exception("Links and subtext not equal in length.")

        print(f"Found {len(links)} links and {len(subtext)} subtext elements.")
        return create_custom_hn(links, subtext)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []


def create_custom_hn(links, subtext):
    print("Creating custom Hacker News list...")
    hn = []
    for index, item in enumerate(links):
        title = subtext[index]
        href = links[index]
        hn.append({"title": title, "link": href})

    print(f"Created list of {len(hn)} stories.")
    return hn


class NewsGui:

    def __init__(self, root):
        print("Initializing GUI...")
        self.root = root
        self.root.title("Hacker News, Compressed")
        self.root.geometry("625x550")

        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.refresh_button = ttk.Button(
            self.mainframe, text="Refresh", command=self.refresh_news
        )
        self.refresh_button.grid(column=0, row=0, sticky=W)

        self.news_canvas = Canvas(self.mainframe, width=600, height=500)
        self.news_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.news_canvas.grid(column=0, row=1, sticky=(N, W, E, S))
        self.news_frame = ttk.Frame(self.news_canvas)
        self.news_scrollbar = ttk.Scrollbar(
            self.mainframe, orient=VERTICAL, command=self.news_canvas.yview
        )
        self.news_scrollbar.grid(column=1, row=1, sticky=(N, S))
        self.news_canvas.configure(yscrollcommand=self.news_scrollbar.set)

        self.news_canvas.create_window((0, 0), window=self.news_frame, anchor="nw")
        self.news_frame.bind("<Configure>", self.on_frame_configure)

        self.news_list = []

        self.refresh_news()

    def on_frame_configure(self, event):
        self.news_canvas.configure(scrollregion=self.news_canvas.bbox("all"))
        self.news_canvas.configure(width=600, height=500)

    def _on_mousewheel(self, event):
        self.news_canvas.yview_scroll(int(-1*(event.delta)), "units")

    def refresh_news(self):
        print("Refreshing news...")
        for widget in self.news_frame.winfo_children():
            widget.destroy()

        self.news_list = fetch_news()
        if self.news_list:
            print("Displaying news stories...")
            self.display_news()
        else:
            print("Failed to fetch news, displaying error message.")
            ttk.Label(self.news_frame, text="Failed to fetch news").grid(
                column=0, row=0, sticky=W
            )

    def display_news(self):
        for index, dic in enumerate(self.news_list):
            json_frame = Frame(
                self.news_frame, relief="flat", borderwidth=0, padx=10, pady=5
            )
            json_frame.grid(column=0, row=index, sticky=W)

            ttk.Label(json_frame, text="{", font=("Helvetica", 12, "bold")).grid(
                row=0, column=0, sticky=W
            )

            for key_index, key in enumerate(dic):
                if key == "link":
                    link_label = ttk.Label(
                        json_frame,
                        text=f"{key}: {dic[key]}",
                        font=("Helvetica", 10, "underline"),
                        cursor="hand2",
                    )
                    link_label.grid(row=key_index + 1, column=0, sticky=W, padx=(10, 0))
                    link_label.bind(
                        "<Button-1>", lambda event, url=dic["link"]: self.callback(url)
                    )
                else:
                    ttk.Label(
                        json_frame, text=f"{key}: {dic[key]}", font=("Helvetica", 10)
                    ).grid(row=key_index + 1, column=0, sticky=W, padx=(10, 0))

            ttk.Label(json_frame, text="}", font=("Helvetica", 12, "bold")).grid(
                row=len(dic) + 1, column=0, sticky=W
            )

    def callback(self, url):
        print(f"Opening URL: {url}")
        webbrowser.open_new_tab(url)


def createGui():
    print("Creating GUI...")
    root = Tk()
    _ = NewsGui(root)

    root.mainloop()

createGui()
