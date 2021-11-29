from dotenv import load_dotenv
load_dotenv()

from os import getenv


TITLE = 'MP3 Player'
WINDOW_SIZE = "600x300"

# Allow resize or not
RESIZE_H = False
RESIZE_W = False

MP3_FOLDER_PATH = getenv('MP3_FOLDER_PATH')
