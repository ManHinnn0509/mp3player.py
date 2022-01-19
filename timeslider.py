import time

import tkinter as tk
from tkinter import *

from mp3player import MP3Player
from config import COLOR_THEME

class TimeSlider:
    def __init__(self, mp3Player: MP3Player) -> None:
        self.mp3Player = mp3Player
        self.master = mp3Player.master

        sliderFrame = Frame(self.master)
        sliderFrame.configure(
            bg=COLOR_THEME["bg_color"]
        )
        self.sliderFrame = sliderFrame

        self.posTime = 0
        self.songLen = 0

        posVar = DoubleVar()
        posVar.set(0)
        self.posVar = posVar

        slider = Scale(
            sliderFrame,
            from_=0, to=0,
            resolution=1,
            orient=HORIZONTAL,
            length=300,
            showvalue=0,
            variable=self.posVar,
            bg=COLOR_THEME["time_slider"]["slider_color"],      # Should be the same as bg_color
            troughcolor=COLOR_THEME["time_slider"]["trough_color"],
            highlightbackground=COLOR_THEME["bg_color"]
        )
        slider.bind("<ButtonRelease-1>", self.dragPosition)
        self.slider = slider

        timeLabel = Label(
            sliderFrame,
            text='- / -',
            fg=COLOR_THEME["time_slider"]["text_color"],
            bg=COLOR_THEME["bg_color"]
        )
        self.timeLabel = timeLabel

        self.slider.grid(row=0, column=0)
        self.timeLabel.grid(row=1, column=0)
        self.sliderFrame.pack(side='bottom')

    def dragPosition(self, event=None):
        if not (self.mp3Player.playedAnySongs):
            return
        
        newPos = round(self.slider.get())

        # Updates the slider
        self.updatePosition(newPos)
        self.mp3Player.playSong(resetPos=False)

    def updatePosition(self, newPos: int):
        """
            Updates the time slider's position
        """

        # An entra second to finish the current play
        if (newPos >= self.songLen + 1):

            if not (self.mp3Player.loopEnabled):
                self.mp3Player.isPlaying = False
                self.posTime += 1
            
            else:
                self.posTime = 0

        else:
            self.posTime = newPos
        
        self.posVar.set(int(newPos))

        self.updateTimeLabel()

    def reset(self):
        """
            Resets the time slider's position & the time lable
        """
        # 0 or -1?
        # self.posTime = 0 if not (self.mp3Player.playedAnySongs) else -1
        self.posTime = 0
        self.posVar.set(0)

        self.updateTimeLabel()

    def updateTimeLabel(self):
        """
            Updates time label
        """
        # Time / seconds formatting
        fPos = time.strftime('%H:%M:%S', time.gmtime(self.posTime))
        fLen = time.strftime('%H:%M:%S', time.gmtime(self.songLen))

        self.slider.configure(to=self.songLen)
        self.timeLabel.config(text=f'{fPos} / {fLen}')
    
    def updateSongLen(self, newLen: int):
        self.songLen = newLen
