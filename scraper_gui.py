from tkinter import *
from tkinter import ttk
import webbrowser

class NewsGui:

    def __init__(self, root, story_list):

        root.title("Hacker News, Only The Best Bits")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        row_count = 1
        for dic in story_list:
            column_count = 1
            for key in dic:
                if column_count == 2:
                    ttk.Button(mainframe, text=dic[key], command=lambda i=dic[key]: self.callback(i)).grid(column=column_count, row=row_count, sticky=W)
                else:
                    ttk.Label(mainframe, text=dic[key]).grid(column=column_count, row=row_count, sticky=W)
                column_count += 1
            row_count += 1

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def callback(self, url):
        webbrowser.open_new_tab(url)

def createGui(story_list):
    root = Tk()
    NewsGui(root, story_list)
    root.mainloop()
