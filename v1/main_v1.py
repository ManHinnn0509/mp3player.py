import os
import time
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

        # In seconds
        self.posTime = 0
        self.songLen = 0

        pygame.init()
        mixer.init()

        self.job = None
        self.sound = None
        self.isPlaying = False
        self.loopEnable = False

        self.__initListbox()
        self.__initButtons()
        self.__initVolumeSlider()
        self.__initPositionSlider()

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

    def __initVolumeSlider(self):
        volumeSlider = Scale(
            self.buttonFrame,
            from_=0, to=100,
            orient=HORIZONTAL,
            resolution=1,
            command=self.__changeVolume
        )

        # Set default value to the slider
        volumeSlider.set(int(self.volume * 100))

        self.volumeSlider = volumeSlider

        # Last row index + 1
        # Otherwise they will overlap
        self.volumeSlider.grid(row=5, column=0)

    def __initPositionSlider(self):
        
        frame = Frame(self.master)
        self.positionFrame = frame

        posVar = DoubleVar()
        posVar.set(0)
        self.posVar = posVar

        slider = Scale(
            frame,
            from_=0, to=0,
            resolution=1,
            length=300,
            orient=HORIZONTAL,
            # command=self.__changePosition,
            showvalue=0,
            variable=self.posVar
        )
        slider.bind("<ButtonRelease-1>", self.__changePosition)
        self.positionSlider = slider
        
        timeLabel = Label(
            frame,
            text='- / -'
        )
        self.timeLabel = timeLabel

        self.positionSlider.grid(row=0, column=0)
        self.timeLabel.grid(row=1, column=0)
        self.positionFrame.pack(side='bottom')

    # ----- End of init functions

    def __changeVolume(self, ignored): 
        value = self.volumeSlider.get()
        
        # The accepted value for set_volume() is between 0 ~ 1
        volume = value / 100
        self.volume = volume

        if (self.sound != None):
            # self.sound.set_volume(self.volume)
            mixer.music.set_volume(self.volume)

    # Listbox (Double click)
    def __changeSong(self, event):
        selectedIndex = event.widget.curselection()[0]
        self.songIndex = selectedIndex
        self.__playSong()
    
    # Prev button click
    def __prevButton(self):
        if (self.songIndex == 0):
            return
        self.songIndex -= 1
        self.__playSong()

    # Next button click
    def __nextButton(self):
        if (self.songIndex == len(self.songs) - 1):
            return
        self.songIndex += 1
        self.__playSong()

    # Loop enabling button
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
            mixer.music.pause()
            self.isPlaying = False
            self.playButton.configure(text='Resume')

        # Resume music, "Resume" -> "Pause"
        else:
            mixer.unpause()
            mixer.music.unpause()
            self.isPlaying = True
            self.playButton.configure(text='Pause')

    # Function that loads and plays .mp3 file
    def __playSong(self, resetPos=True):

        selectedSongName = self.songs[self.songIndex]
        self.master.title(selectedSongName)

        mp3Path = f'{self.mp3DirPath}\\{selectedSongName}'
        mp3Path = mp3Path.replace('\\', '/')

        # Stop any already playing songs
        if (self.sound != None):
            self.sound.stop()
        
        self.isPlaying = False

        # Cancel previous counting
        if (self.job != None):
            self.master.after_cancel(self.job)
            self.job = None
        
        try:
            
            # This line might throw pygame.error
            self.sound = mixer.Sound(mp3Path)

            self.isPlaying = True
            self.playButton.configure(text='Pause')

            # Reset the time position slider & update info
            self.songLen = int(self.sound.get_length())
            if (resetPos):
                self.__changePosition(resetPos=True)
            
            # Loop inf. times if pass in -1
            loop = -1 if (self.loopEnable) else 0
            # self.sound.play(loops=loop)
            # self.sound.set_volume(self.volume)

            mixer.music.load(mp3Path)
            mixer.music.play(loops=loop, start=self.posTime)
            mixer.music.set_volume(self.volume)
            
            # Starts counting & moving time slider
            self.__countPosition()
            
        except Exception as e:
        # except pygame.error as e:
            print(traceback.format_exc())
            print(f'[ERROR] Unable to open file [{selectedSongName}]')

    # For auto-counting seconds
    def __countPosition(self):
        self.job = self.master.after(1000, self.__countPosition)
        # print('[DEBUG] Calling self.__changePosition()')
        self.__changePosition(counting=True, setPos=True)

        # print(f'[DEBUG] Volume setted to {value}')

    # For time position slider changing
    # Including dragged by user, auto-counting
    def __changePosition(self, ignored=None, resetPos=False, counting=False, setPos=False):

        # Song paused
        if (counting) and (setPos):
            if not (self.isPlaying):
                return

        if not (resetPos):
            # Dragged by user
            if not (counting):
                posValue = int(self.positionSlider.get())
                self.posTime = posValue

                self.__playSong(resetPos=False)
                return

            # Auto-counting
            else:
                # Song not ended, keep counting
                if (self.posTime != self.songLen):
                    self.posTime += 1

                # Song is ended
                else:
                    # Loop is enabled so start again
                    if (self.loopEnable):
                        self.posTime = 0
                    
                    # Set isPlaying to False
                    # Since song is ended and loop not enabled
                    else:
                        self.isPlaying = False
                        return
        
        # Reset position
        else:
            # Should be 0 or -1?
            self.posTime = -1

        # Changed. Solution: https://stackoverflow.com/questions/4038517/tkinter-set-a-scale-value-without-triggering-callback
        self.posVar.set(self.posTime)

        # Time / seconds formatting
        fPos = time.strftime('%H:%M:%S', time.gmtime(self.posTime))
        fLen = time.strftime('%H:%M:%S', time.gmtime(self.songLen))
        
        # Update text
        self.positionSlider.configure(to=self.songLen)
        self.timeLabel.config(text=f'{fPos} / {fLen}')

    # For init.
    def __getMP3(self):
        return [i for i in os.listdir(self.mp3DirPath) if (i.endswith('.mp3'))]

def main():
    root = tk.Tk()
    mp3Player = MP3Player(root, MP3_FOLDER_PATH)

    root.mainloop()

if (__name__ == '__main__'):
    main()
