import os
import traceback

import tkinter as tk
from tkinter import *
import pygame
from pygame import mixer

from config import *

class MP3Player:
    
    def __init__(self, dirPath: str) -> None:

        from songlist import SongList
        from controlmenu import ControlMenu
        from timeslider import TimeSlider
        from statusbar import StatusBar

        master = Tk()
        self.master = master

        master.title(TITLE)
        master.geometry(WINDOW_SIZE)
        master.resizable(RESIZE_W, RESIZE_H)

        pygame.init()
        mixer.init()
        self.mixer = mixer

        # --- Variables
        self.dirPath = dirPath if (dirPath[-1] == '\\' or dirPath[-1] == '/') else dirPath
        self.songs = self.__getMP3()

        self.songIndex = 0

        self.volume = 50 / 100

        self.isPlaying = False
        self.loopEnabled = False
        self.playedAnySongs = False

        self.job = None
        
        # --- Widgets

        statusBar = StatusBar(mp3Player=self)
        self.statusBar = statusBar

        songList = SongList(mp3Player=self)
        self.songList = songList

        controlMenu = ControlMenu(mp3Player=self)
        self.controlMenu = controlMenu

        timeSlider = TimeSlider(mp3Player=self)
        self.timeSlider = timeSlider

        self.lyricsDisplay = None

    def playSong(self, resetPos=True):
        self.playedAnySongs = True

        selectedSong = self.songs[self.songIndex]
        songPath = f'{self.dirPath}\\{selectedSong}'.replace('\\', '/')

        # Cancel previous counting
        if (self.job != None):
            self.master.after_cancel(self.job)
            self.job = None
        
        self.isPlaying = False

        try:
            # This line might throw error
            songLen = int(self.mixer.Sound(songPath).get_length())

            # Update the total seconds / time to the new song's
            self.timeSlider.updateSongLen(songLen)

            # Change the window's title to the song name
            self.master.title(selectedSong)

            self.isPlaying = True
            # Reset the button's text since it's playing now
            self.controlMenu.pauseResumeButton.config(text='Pause')

            # Resets the counting
            if (resetPos):
                # Clears the previous lyrics lines
                self.statusBar.updateText('')
                from lyricsdisplay import LyricsDisplay
                self.lyricsDisplay = LyricsDisplay(
                    mp3Player=self, dirPath=MP3_FOLDER_PATH, mp3Name=selectedSong
                )

                self.timeSlider.changePosition(resetPos=True)

            # Loop inf. times if pass in -1
            loop = -1 if (self.loopEnabled) else 0

            self.mixer.music.load(songPath)
            self.mixer.music.play(loops=loop, start=self.timeSlider.posTime)    # This throws exception too
            self.mixer.music.set_volume(self.volume)

            self.__countPosition()

        except Exception as e:
            print(traceback.format_exc())
            print(f'[ERROR] Unable to open file [{selectedSong}]')

    def __countPosition(self):
        self.job = self.master.after(1000, self.__countPosition)

        self.timeSlider.changePosition(counting=True, setPos=True)
        # print(self.timeSlider.posTime)

        # Always keep this part under the changePosition() call
        if (self.lyricsDisplay != None):
            if (self.lyricsDisplay.hasLyrics()):
                self.lyricsDisplay.displayLyrics()

    # For init.
    def __getMP3(self):
        return [i for i in os.listdir(self.dirPath) if (i.endswith('.mp3'))]
    
    def start(self):
        self.master.mainloop()