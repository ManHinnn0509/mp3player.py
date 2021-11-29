import sys
sys.path.append('..')

import tkinter as tk
from tkinter import *

from mp3player import MP3Player

class SongList:
    def __init__(self, mp3Player: MP3Player) -> None:
        self.mp3Player = mp3Player
        self.master = mp3Player.master
        
        listboxFrame = Frame(self.master)
        self.listboxFrame = listboxFrame

        listbox = Listbox(
            listboxFrame,
            listvariable=StringVar(value=self.mp3Player.songs)
        )
        listbox.bind('<Double-1>', self.__clickToChangeSong)
        self.listbox = listbox

        scrollbar = Scrollbar(
            listboxFrame,
            orient='vertical',
            command=listbox.yview
        )
        self.scrollbar = scrollbar

        self.listbox['yscrollcommand'] = self.scrollbar.set

        self.listbox.pack(fill=tk.Y, expand=True)
        self.listboxFrame.pack(fill=tk.Y, side='left')

    def __clickToChangeSong(self, event):
        selectedIndex = event.widget.curselection()[0]
        self.mp3Player.songIndex = selectedIndex
        self.mp3Player.__playSong()