import random

import tkinter as tk
from tkinter import *

from pygame import mixer

from mp3player import MP3Player
from config import COLOR_THEME

class ControlMenu:

    PAUSE_TEXT = "Pause ⏸"
    RESUME_TEXT = "Resume ▶️"

    LOOP_ENABLED_TEXT = "Loop 🔁\n(Enabled)"
    LOOP_DISABLED_TEXT = "Loop 🔁\n(Disabled)"

    RANDOM_TEXT = "Random"

    def __init__(self, mp3Player: MP3Player) -> None:
        self.mp3Player = mp3Player
        self.master = mp3Player.master

        self.buttonHeight = 3
        self.buttonWidth = 13

        # Create the frame for this menu
        menuFrame = Frame(self.master)
        menuFrame.configure(
            bg=COLOR_THEME["bg_color"],
            highlightbackground=COLOR_THEME["bg_color"]
        )
        self.menuFrame = menuFrame

        # Previous song button
        prevButton = Button(
                menuFrame, text='▲ Previous ▲',
                width=self.buttonWidth, height=self.buttonHeight,
                command=self.prev,
                fg=COLOR_THEME["buttons"]["previous"]["text_color"],
                bg=COLOR_THEME["buttons"]["previous"]["bg_color"]
        )
        self.prevButton = prevButton
        self.prevButton.grid(row=1, column=0)

        # Pause / resume button
        pauseResumeButton = Button(
                menuFrame, text=self.PAUSE_TEXT,
                width=self.buttonWidth, height=self.buttonHeight,
                command=self.pauseResume,
                fg=COLOR_THEME["buttons"]["pause"]["text_color"],
                bg=COLOR_THEME["buttons"]["pause"]["bg_color"]
        )
        self.pauseResumeButton = pauseResumeButton
        self.pauseResumeButton.grid(row=2, column=0)

        # Next song button
        nextButton = Button(
                menuFrame, text='▼ Next ▼',
                width=self.buttonWidth, height=self.buttonHeight,
                command=self.next,
                fg=COLOR_THEME["buttons"]["next"]["text_color"],
                bg=COLOR_THEME["buttons"]["next"]["bg_color"]
        )
        self.nextButton = nextButton
        self.nextButton.grid(row=3, column=0)

        # Loop enabling / disabling button
        loopButton = Button(
                menuFrame, text=self.LOOP_DISABLED_TEXT,
                width=self.buttonWidth, height=self.buttonHeight,
                command=self.__loopButton,
                fg=COLOR_THEME["buttons"]["loop"]["text_color"],
                bg=COLOR_THEME["buttons"]["loop"]["bg_color"]
        )
        self.loopButton = loopButton
        self.loopButton.grid(row=4, column=0)

        randomButton = Button(
            menuFrame, text=self.RANDOM_TEXT,
            width=self.buttonWidth, height=self.buttonHeight,
            command=self.__playRandomSong,
                fg=COLOR_THEME["buttons"]["random"]["text_color"],
                bg=COLOR_THEME["buttons"]["random"]["bg_color"]
        )
        self.randomButton = randomButton
        self.randomButton.grid(row=5, column=0)

        volumeLabel = Label(
            self.menuFrame,
            text = f"{int(self.mp3Player.volume * 100)}",
            fg=COLOR_THEME["volume_control"]["text_color"],
            bg=COLOR_THEME["bg_color"]
        )
        self.volumeLabel = volumeLabel
        self.volumeLabel.grid(row=6, column=0)

        # Volume slider
        volumeSlider = Scale(
            self.menuFrame,
            from_=0, to=100,
            showvalue=0,
            orient=HORIZONTAL,
            resolution=1,
            command=self.__changeVolume,
            highlightbackground=COLOR_THEME["bg_color"],
            bg=COLOR_THEME["volume_control"]["slider_color"]
        )

        # Set default value to the slider
        volumeSlider.set(int(self.mp3Player.volume * 100))

        self.volumeSlider = volumeSlider
        self.volumeSlider.grid(row=7, column=0)

        # Pack the frame
        self.menuFrame.pack(fill=tk.Y, side='right')
    
    def prev(self):
        if (self.mp3Player.songIndex != 0):
            self.mp3Player.songIndex -= 1
            self.mp3Player.selectedSong = self.mp3Player.songs[self.mp3Player.songIndex]
            self.mp3Player.playSong()
    
    def pauseResume(self, ignored=None):
        mp3Player = self.mp3Player

        # Not gonna apply any changes if no songs were being played
        if not (mp3Player.playedAnySongs):
            return

        # Song is playing, change it from Pause to Resume
        if (mp3Player.isPlaying):
            mp3Player.mixer.pause()
            mp3Player.mixer.music.pause()

            mp3Player.isPlaying = False
            self.pauseResumeButton.configure(text=self.RESUME_TEXT)

        # Song ISN'T playing, change it from Resume to Pause
        else:
            mp3Player.mixer.unpause()
            mp3Player.mixer.music.unpause()

            mp3Player.isPlaying = True
            self.pauseResumeButton.configure(text=self.PAUSE_TEXT)
    
    def next(self):
        if (self.mp3Player.songIndex != len(self.mp3Player.songs) - 1):
            self.mp3Player.songIndex += 1
            self.mp3Player.selectedSong = self.mp3Player.songs[self.mp3Player.songIndex]
            self.mp3Player.playSong()

    def __loopButton(self):
        if (self.mp3Player.loopEnabled):
            self.mp3Player.loopEnabled = False
            self.loopButton.configure(text=self.LOOP_DISABLED_TEXT)
        
        else:
            self.mp3Player.loopEnabled = True
            self.loopButton.configure(text=self.LOOP_ENABLED_TEXT)

    def __changeVolume(self, event):
        value = self.volumeSlider.get()

        # The accepted value for set_volume() is between 0 ~ 1
        volume = value / 100
        self.mp3Player.volume = volume

        # Updates the display value
        self.volumeLabel.configure(text=f"{value}")

        # CHANGE VOLUME CODE HERE
        self.mp3Player.mixer.music.set_volume(volume)
    
    def __playRandomSong(self):
        songAmount = len(self.mp3Player.songs)
        if (songAmount == 0):
            return
        
        # 0 <= i < len(songList)
        i = int(random.randrange(0, songAmount))

        self.mp3Player.songIndex = i
        self.mp3Player.playSong()
        