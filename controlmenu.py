import tkinter as tk
from tkinter import *

from pygame import mixer

from mp3player import MP3Player

class ControlMenu:

    def __init__(self, mp3Player: MP3Player) -> None:
        self.mp3Player = mp3Player
        self.master = mp3Player.master

        self.buttonHeight = 3
        self.buttonWidth = 13

        # Create the frame for this menu
        menuFrame = Frame(self.master)
        self.menuFrame = menuFrame

        # Previous song button
        prevButton = Button(
                menuFrame, text='Previous',
                width=self.buttonWidth, height=self.buttonHeight,
                command=self.__prevButton
        )
        self.prevButton = prevButton
        self.prevButton.grid(row=1, column=0)

        # Pause / resume button
        pauseResumeButton = Button(
                menuFrame, text='Pause',
                width=self.buttonWidth, height=self.buttonHeight,
                command=self.__pauseResume
        )
        self.pauseResumeButton = pauseResumeButton
        self.pauseResumeButton.grid(row=2, column=0)

        # Next song button
        nextButton = Button(
                menuFrame, text='Next',
                width=self.buttonWidth, height=self.buttonHeight,
                command=self.__nextButton
        )
        self.nextButton = nextButton
        self.nextButton.grid(row=3, column=0)

        # Loop enabling / disabling button
        loopButton = Button(
                menuFrame, text='Loop\n(Disabled)',
                width=self.buttonWidth, height=self.buttonHeight,
                command=self.__loopButton
        )
        self.loopButton = loopButton
        self.loopButton.grid(row=4, column=0)

        # Volume slider
        volumeSlider = Scale(
            self.menuFrame,
            from_=0, to=100,
            orient=HORIZONTAL,
            resolution=1,
            command=self.__changeVolume
        )

        # Set default value to the slider
        volumeSlider.set(int(self.mp3Player.volume * 100))

        self.volumeSlider = volumeSlider
        self.volumeSlider.grid(row=5, column=0)

        # Pack the frame
        self.menuFrame.pack(fill=tk.Y, side='right')
    
    def __prevButton(self):
        if (self.mp3Player.songIndex == 0):
            self.mp3Player.songIndex -= 1
            self.mp3Player.__playSong()
    
    def __pauseResume(self):
        mp3Player = self.mp3Player

        # Not gonna apply any changes if no songs were being played
        if not (mp3Player.playedAnySongs):
            return

        # Song is playing, change it from Pause to Resume
        if (mp3Player.isPlaying):
            mp3Player.mixer.pause()
            mp3Player.mixer.music.pause()

            mp3Player.isPlaying = False
            self.pauseResumeButton.configure(text='Resume')

        # Song ISN'T playing, change it from Resume to Pause
        else:
            mp3Player.mixer.unpause()
            mp3Player.mixer.music.unpause()

            mp3Player.isPlaying = True
            self.pauseResumeButton.configure(text='Pause')
    
    def __nextButton(self):
        if (self.mp3Player.songIndex != len(self.mp3Player.songs) - 1):
            self.mp3Player.songIndex += 1
            self.mp3Player.__playSong()

    def __loopButton(self):
        if (self.mp3Player.loopEnabled):
            self.mp3Player.loopEnabled = False
            self.loopButton.configure(text='Loop\n(Disabled)')
        
        else:
            self.mp3Player.loopEnabled = True
            self.loopButton.configure(text='Loop\n(Enabled)')

    def __changeVolume(self, event):
        value = self.volumeSlider.get()

        # The accepted value for set_volume() is between 0 ~ 1
        volume = value / 100
        self.mp3Player.volume = volume

        # CHANGE VOLUME CODE HERE
        self.mp3Player.mixer.music.set_volume(volume)