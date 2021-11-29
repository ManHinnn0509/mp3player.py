import tkinter as tk
from tkinter import *

from mp3player import MP3Player

class StatusBar:

    def __init__(self, mp3Player: MP3Player) -> None:
        self.mp3Player = mp3Player
        self.master = mp3Player.master

        text = StringVar()
        text.set('')
        self.text = text

        statusBar = Label(
            self.master,
            textvariable=self.text,
            relief=SUNKEN,
            anchor='w'
        )
        self.statusBar = statusBar

        self.statusBar.pack(side=BOTTOM, fill=X)
    
    def updateText(self, newText: str):
        self.text.set(newText)
