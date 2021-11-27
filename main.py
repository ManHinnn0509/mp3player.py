import os
import traceback

import tkinter as tk
from tkinter import *
import pygame
from pygame import mixer

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
        self.volume = 50 / 100

        pygame.init()
        mixer.init()
        self.sound = None
        self.isPlaying = False
        self.loopEnable = False

        self.__initListbox()
        self.__initButtons()
        self.__initSlider()
    
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

        self.listbox.pack(fill=tk.Y, expand=True)
        self.listboxFrame.pack(fill=tk.Y, side='left')
     
    def __initSlider(self):
        slider = Scale(
            self.buttonFrame,
            from_=0, to=100,
            orient=HORIZONTAL,
            resolution=1,
            command=self.__changeVolume
        )

        # Set default value to the slider
        slider.set(50)

        self.slider = slider

        # Last row index + 1
        # Otherwise they will overlap
        self.slider.grid(row=5, column=0)

    def __changeVolume(self, ignored): 
        value = self.slider.get()
        
        # The accepted value for set_volume() is between 0 ~ 1
        volume = value / 100
        self.volume = volume

        if (self.sound != None):
            self.sound.set_volume(self.volume)

        # print(f'[DEBUG] Volume setted to {value}')


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
                width=buttonWidth, height=buttonHeight,
                command=self.__pauseResume
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

        loopButton = Button(
                buttonFrame, text='Loop\n(Disabled)',
                width=buttonWidth, height=buttonHeight,
                command=self.__loopButton
        )
        self.loopButton = loopButton
        self.loopButton.grid(row=4, column=0)

        self.buttonFrame.pack(fill=tk.Y, side='right')
    
    # Listbox (Double click)
    def __changeSong(self, event):
        selectedIndex = event.widget.curselection()[0]
        self.songIndex = selectedIndex
        self.__playSong(loopPlay=False)
    
    # Prev button click
    def __prevButton(self):
        if (self.songIndex == 0):
            return
        self.songIndex -= 1
        self.__playSong(loopPlay=False)

    # Next button click
    def __nextButton(self):
        if (self.songIndex == len(self.songs) - 1):
            return
        self.songIndex += 1
        self.__playSong(loopPlay=False)

    def __loopButton(self):
        if (self.loopEnable):
            self.loopEnable = False
            self.loopButton.configure(text='Loop\n(Disabled)')
        else:
            self.loopEnable = True
            self.loopButton.configure(text='Loop\n(Enabled)')

    # Pause / resume button click
    def __pauseResume(self):
        if (self.sound == None):
            return

        # Pause music, "Pause" -> "Resume"
        if (self.isPlaying):
            mixer.pause()
            self.isPlaying = False
            self.playButton.configure(text='Resume')

        # Resume music, "Resume" -> "Pause"
        else:
            mixer.unpause()
            self.isPlaying = True
            self.playButton.configure(text='Pause')

    def __playSong(self, loopPlay=False):
        '''
        if (mixer.Channel(0).get_busy()):
            print('BUSY')
            return
        '''
        
        '''
        if (loopPlay):
            if not (self.loopEnable):
                return
        '''

        selectedSongName = self.songs[self.songIndex]
        self.master.title(selectedSongName)

        mp3Path = f'{self.mp3DirPath}\\{selectedSongName}'
        mp3Path = mp3Path.replace('\\', '/')

        if (self.sound != None):
            self.sound.stop()

        try:
            self.isPlaying = True
            self.playButton.configure(text='Pause')
            
            # This line might throw pygame.error
            self.sound = mixer.Sound(mp3Path)
            
            # Loop inf. times if pass in -1
            # loop = -1 if (self.loopEnable) else 0
            self.sound.play(loops=(-1 if (self.loopEnable) else 0))
            self.sound.set_volume(self.volume)

            # Create recursive call for enabling loop while playing
            # And also added loop checking
            # self.sound.play()
            # self.__playSong(loopPlay=True)

        except Exception as e:
        # except pygame.error as e:
            print(traceback.format_exc())
            print(f'[ERROR] Unable to open file [{selectedSongName}]')

    # For init.
    def __getMP3(self):
        return [i for i in os.listdir(self.mp3DirPath) if (i.endswith('.mp3'))]

def main():
    root = tk.Tk()
    mp3Player = MP3Player(root, MP3_FOLDER_PATH)

    root.mainloop()

if (__name__ == '__main__'):
    main()
