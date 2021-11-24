import os

import tkinter as tk
from tkinter import *

from config import *

class MP3Player:
    def __init__(self, master: tk.Tk, mp3DirPath: str) -> None:
        self.master = master
        self.mp3DirPath = mp3DirPath

        master.title(TITLE)
        master.geometry(WINDOW_SIZE)
        master.resizable(RESIZE_W, RESIZE_H)

        self.songs = self.__getMP3()
        self.songIndex = 0

        self.__initListbox()
        self.__initButtons()
    
    def __initListbox(self):
        master = self.master

        listboxFrame = Frame(master)
        self.listboxFrame = listboxFrame

        listbox = Listbox(
            listboxFrame,
            listvariable=StringVar(value=self.songs)
        )
        listbox.bind('<Double-1>', self.__changeSong)
        self.listbox = listbox

        scrollbar = Scrollbar(
            listboxFrame,
            orient='vertical',
            command=listbox.yview
        )
        self.scrollbar = scrollbar

        self.listbox['yscrollcommand'] = self.scrollbar.set

        # self.listbox.grid(sticky='E')
        # self.listboxFrame.grid(sticky='E')

        self.listbox.pack(fill=tk.Y, expand=True)
        self.listboxFrame.pack(fill=tk.Y, side='left')
    
    def __initButtons(self):
        master = self.master
        buttonHeight = 3
        buttonWidth = 10

        buttonFrame = Frame(master)
        self.buttonFrame = buttonFrame
        
        prevButton = Button(
                buttonFrame, text='Previous',
                width=buttonWidth, height=buttonHeight,
                command=self.__prevButton
        )
        self.prevButton = prevButton
        self.prevButton.grid(row=1, column=0)

        playButton = Button(
                buttonFrame, text='Pause',
                width=buttonWidth, height=buttonHeight
        )
        self.playButton = playButton
        self.playButton.grid(row=2, column=0)

        nextButton = Button(
                buttonFrame, text='Next',
                width=buttonWidth, height=buttonHeight,
                command=self.__nextButton
        )
        self.nextButton = nextButton
        self.nextButton.grid(row=3, column=0)

        self.buttonFrame.pack(fill=tk.Y, side='right')
    
    # Listbox
    def __changeSong(self, event):
        selectedIndex = event.widget.curselection()[0]
        self.songIndex = selectedIndex
        self.__playSong()
    
    def __prevButton(self):
        if (self.songIndex == 0):
            return
        self.songIndex -= 1
        self.__playSong()

    def __nextButton(self):
        if (self.songIndex == len(self.songs) - 1):
            return
        self.songIndex += 1
        self.__playSong()

    def __getMP3(self):
        return [i for i in os.listdir(self.mp3DirPath) if (i.endswith('.mp3'))]

    def __playSong(self):
        selectedSongName = self.songs[self.songIndex]
        print(selectedSongName)



def main():
    root = tk.Tk()
    mp3Player = MP3Player(root, MP3_FOLDER_PATH)

    root.mainloop()

if (__name__ == '__main__'):
    main()
