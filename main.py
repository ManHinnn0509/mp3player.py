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

        listboxFrame = Frame(master)
        self.listboxFrame = listboxFrame

        self.songs = self.__getMP3()

        listbox = Listbox(
            listboxFrame,
            listvariable=StringVar(value=self.songs)
        )
        listbox.bind('<Double-1>', self.__changeSong)
        self.listbox = listbox

        scrollbar = Scrollbar(
            listboxFrame,
            orient='vertical',
            command=listbox.yview
        )
        self.scrollbar = scrollbar

        self.listbox['yscrollcommand'] = self.scrollbar.set

        # self.listbox.grid(sticky='E')
        # self.listboxFrame.grid(sticky='E')

        self.listbox.pack(fill=tk.Y, expand=True)
        self.listboxFrame.pack(fill=tk.Y, side='left')

    def __changeSong(self, event):
        selectedIndex = event.widget.curselection()[0]
        selectedSongName = self.songs[selectedIndex]
        print(selectedSongName)

    def __getMP3(self):
        return [i for i in os.listdir(MP3_FOLDER_PATH) if (i.endswith('.mp3'))]

def main():
    root = tk.Tk()
    mp3Player = MP3Player(root)

    root.mainloop()

if (__name__ == '__main__'):
    main()
