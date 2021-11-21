import os

import tkinter as tk
from tkinter import *

from config import *

class MP3Player:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master

        master.title(TITLE)
        master.geometry(WINDOW_SIZE)
        master.resizable(RESIZE_W, RESIZE_H)

        frame = Frame(master)
        self.frame = frame

        listbox = Listbox(frame)
        self.listbox = listbox
        self.__addContent()

    def __addContent(self):
        # https://stackoverflow.com/questions/46625722/how-to-list-files-in-a-folder-to-a-tk-listbox-python3
        dirContent = [i for i in os.listdir() if (i.endswith('.mp3'))]

        counter = 1
        for mp3 in dirContent:
            self.listbox.insert(counter, mp3)
            counter += 1

def main():
    root = tk.Tk()
    mp3Player = MP3Player(root)

    root.mainloop()

if (__name__ == '__main__'):
    main()