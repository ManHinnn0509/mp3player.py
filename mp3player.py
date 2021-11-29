import os

import tkinter as tk
from tkinter import *
import pygame
from pygame import mixer

from config import *

class MP3Player:
    
    def __init__(self, dirPath: str) -> None:
        from songlist import SongList
        from controlmenu import ControlMenu

        master = Tk()
        self.master = master

        master.title(TITLE)
        master.geometry(WINDOW_SIZE)
        master.resizable(RESIZE_W, RESIZE_H)

        pygame.init()
        mixer.init()
        self.mixer = mixer

        # --- Variables
        self.dirPath = dirPath
        self.songs = self.__getMP3()

        self.songIndex = 0

        self.volume = 50 / 100

        self.isPlaying = False
        self.loopEnabled = False
        self.playedAnySongs = False

        # --- Widgets
        songList = SongList(mp3Player=self)
        self.songList = songList

        controlMenu = ControlMenu(mp3Player=self)
        self.controlMenu = controlMenu

    def __playSong(self):
        self.playedAnySongs = True

    # For init.
    def __getMP3(self):
        return [i for i in os.listdir(self.dirPath) if (i.endswith('.mp3'))]
    
    def start(self):
        self.master.mainloop()