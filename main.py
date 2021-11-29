from mp3player import MP3Player
from config import MP3_FOLDER_PATH

def main():
    mp3Player = MP3Player(MP3_FOLDER_PATH)
    mp3Player.start()

if (__name__ == '__main__'):
    main()