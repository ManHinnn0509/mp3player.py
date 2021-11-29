import os

import tkinter as tk
from tkinter import *
import pygame
from pygame import mixer

from config import *

class MP3Player:
    
    def __init__(self, dirPath: str) -> None:
        from songlist import SongList
        
        self.dirPath = dirPath
        self.songs = self.__getMP3()

        master = Tk()
        self.master = master

        master.title(TITLE)
        master.geometry(WINDOW_SIZE)
        master.resizable(RESIZE_W, RESIZE_H)

        songList = SongList(mp3Player=self)
        self.songList = songList

    def __playSong(self):
        pass

    # For init.
    def __getMP3(self):
        return [i for i in os.listdir(self.dirPath) if (i.endswith('.mp3'))]
    
    def start(self):
        self.master.mainloop()