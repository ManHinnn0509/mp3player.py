import sys
sys.path.append('..')

import tkinter as tk
from tkinter import *

from mp3player import MP3Player
from config import SONG_LIST_TEXT_COLOR

class SongList:
    def __init__(self, mp3Player: MP3Player) -> None:
        self.mp3Player = mp3Player
        self.master = mp3Player.master
        
        listboxFrame = Frame(self.master)
        self.listboxFrame = listboxFrame

        listbox = Listbox(
            listboxFrame,
            listvariable=StringVar(value=self.mp3Player.songs),
            fg=SONG_LIST_TEXT_COLOR
        )
        listbox.bind('<Double-1>', self.__clickToChangeSong)
        listbox.bind('<Button-3>', self.__refresh)
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

    def __refresh(self, event):
        self.mp3Player.songs = self.mp3Player.getMP3()
        self.listbox.configure(
            listvariable=StringVar(value=self.mp3Player.getMP3())
        )

    def __clickToChangeSong(self, event):
        selectedIndex = event.widget.curselection()[0]
        self.mp3Player.songIndex = selectedIndex
        self.mp3Player.playSong()