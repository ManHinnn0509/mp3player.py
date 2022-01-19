from dotenv import load_dotenv
load_dotenv()

from os import getenv
from util.file_utils import readJSON_File

# Path to the directory of .mp3 files
MP3_FOLDER_PATH = getenv('MP3_FOLDER_PATH')

TITLE = 'MP3 Player by ManHinnn0509'
WINDOW_SIZE = "600x350"

# Allow resize or not
RESIZE_H = False
RESIZE_W = False

COLOR_THEME = readJSON_File("./themes/default.json")

# Color options
SONG_LIST_TEXT_COLOR = '#0000FF'
LYRICS_DISPLAY_TEXT_COLOR = '#FF00FF'