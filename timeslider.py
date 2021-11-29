import time

import tkinter as tk
from tkinter import *

from mp3player import MP3Player

class TimeSlider:
    def __init__(self, mp3Player: MP3Player) -> None:
        self.mp3Player = mp3Player
        self.master = mp3Player.master

        sliderFrame = Frame(self.master)
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
            variable=self.posVar
        )
        slider.bind("<ButtonRelease-1>", self.changePosition)
        self.slider = slider

        timeLabel = Label(
            sliderFrame,
            text='- / -'
        )
        self.timeLabel = timeLabel

        self.slider.grid(row=0, column=0)
        self.timeLabel.grid(row=1, column=0)
        self.sliderFrame.pack(side='bottom')

    def changePosition(self, event=None, resetPos=False, counting=False, setPos=False):

        """
            Parameters:
            - event: Ignored. Passed when callback
            - resetPos: Resets the position
            - counting: True for song playing & counting how many seconds passed
            - setPos: True for song playing
        """
        mp3Player = self.mp3Player

        if not (mp3Player.playedAnySongs):
            return
        
        # Song paused. So do nothing and return
        if (counting) and (setPos):
            if not (mp3Player.isPlaying):
                return
        
        # Reset the position by setting it to -1
        # Not 0 is because there will be a counting being started soon
        if (resetPos):
            self.posTime = -1

        else:
            # Dragged by user
            if not (counting):
                self.posTime = int(self.slider.get())
                
                mp3Player.playSong(resetPos=False)
                return
            
            # Auto counting
            else:
                # Song is not ended. Keep counting
                if (self.posTime != self.songLen):
                    self.posTime += 1
                
                # Song is ended
                else:
                    # Ended but loop is enabled. Reset time / position
                    if (mp3Player.loopEnabled):
                        self.posTime = 0
                    
                    # Ended and loop is not enabled.
                    # Set isPlaying to False then return
                    else:
                        mp3Player.isPlaying = False
                        return
        
        # https://stackoverflow.com/questions/4038517/tkinter-set-a-scale-value-without-triggering-callback
        self.posVar.set(self.posTime)

        # Time / seconds formatting
        fPos = time.strftime('%H:%M:%S', time.gmtime(self.posTime))
        fLen = time.strftime('%H:%M:%S', time.gmtime(self.songLen))

        self.slider.configure(to=self.songLen)
        self.timeLabel.config(text=f'{fPos} / {fLen}')
    
    def updateSongLen(self, newLen: int):
        self.songLen = newLen
