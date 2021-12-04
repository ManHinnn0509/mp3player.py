from mp3player import MP3Player

class LyricsDisplay:
    def __init__(self, mp3Player: MP3Player, dirPath: str, mp3Name: str) -> None:
        self.mp3Player = mp3Player
        self.master = mp3Player.master

        self.dirPath = dirPath
        self.mp3Name = mp3Name

        self.songName = mp3Name[:-4]

        self.filePath = f'{dirPath}/{self.songName}.lrc'
        self.lrcContent = self.__readLRC()

        self.lyricsDict = None
        if (self.lrcContent != None):
            parser = LRC_Parser(self.lrcContent)
            self.lyricsDict = parser.lrcDict
        
        self.hasLyrics = self.__hasLyrics()
    
    def displayLyrics(self):
        sec = self.mp3Player.timeSlider.posTime

        # Might can work on this part
        # Since the dict() uses int as key
        # Maybe I can change it to 1 decimal point float like 10.2 etc.
        # The lyrics should be more accurate

        if (sec < 0):
            sec = 0
        
        # For float value support
        sec = f'{sec:.1f}'
        
        lyrics = self.lyricsDict.get(sec, None)

        # Debug
        # print(f'sec={sec} | lyrics={lyrics}')

        if (lyrics != None):
            self.mp3Player.statusBar.updateText(lyrics)
    
    def __hasLyrics(self):
        if (self.lrcContent == None):
            # print('self.lrcContent == None')
            return False
        
        if (self.lyricsDict == None):
            # print('self.lyricsDict == None')
            return False

        if (len(self.lyricsDict) == 0):
            # print('len(self.lyricsDict) == 0')
            return False
        
        return True

    def __readLRC(self, encoding='UTF-8'):
        try:
            with open(self.filePath, 'r', encoding=encoding) as f:
                return f.read()
        except:
            return None

"""
    Just a simple class I created.
    This class is for converting the .lrc file content into a dict() like this:
    {
        "31":"She's got a smile it seems to me",
        "35":"Reminds me of childhood memories",
        "38":"Where everything",
        "40":"Was as fresh as the bright blue sky",
        "46":"Now and then when I see her face",
        "50":"She takes me away to that special place",
        "53":"And if I'd stare too long",
        "55":"I'd probably break down and cry",
        "61":"Oh, oh, oh",
        "64":"Sweet child o' mine",
        "69":"Oh, oh, oh, oh",
        "71":"Sweet love of mine",
        "92":"She's got eyes of the bluest skies",
        "96":"As if they thought of rain",
        "100":"I hate to look into those eyes",
        "103":"And see an ounce of pain",
        "107":"Her hair reminds me of a warm safe place",
        "111":"Where as a child I'd hide",
        "115":"And pray for the thunder",
        "117":"And the rain",
        "119":"To quietly pass me by",
        "123":"Oh, oh, oh",
        "125":"Sweet child o' mine",
        "130":"Oh, oh, oh, oh",
        "133":"Sweet love of mine",
        "138":"Oh, oh, oh, oh",
        "140":"Sweet child o' mine",
        "146":"Oh, oh, oh, oh",
        "149":"Sweet love of mine",
        "222":"Oh, oh, oh, oh",
        "223":"Oh oh sweet love of mine",
        "224":"Where do we go now?",
        "225":"Where do we go?",
        "229":"(Where do we go now?)",
        "233":"Oh where do we go now? (Where do we go?)",
        "235":"Where do we go? (Sweet child)",
        "237":"Oh where do we go now?",
        "240":"Ay ay ay ay (where do we go now, where do we go)",
        "245":"Oh where do we go now?",
        "247":"Where do we go?",
        "250":"Oh, where do we go now?",
        "255":"Oh, where do we go?",
        "258":"Oh where do we go now?",
        "262":"Where do we go?",
        "265":"Oh, where do we go now?",
        "269":"No, no, no, no, no, no",
        "271":"Sweet child",
        "273":"Sweet child of mine"
    }

    Uses second as KEY and the lyrics as VALUE
"""
class LRC_Parser:

    def __init__(self, lrcContent: str) -> None:
        self.lrcContent = lrcContent
        self.lrcLines = [i for i in lrcContent.split('\n') if (i != '\n' or i != '')]

        self.offset = self.__getOffset()
        self.lrcDict = self.__processContent()
    
    def __getOffset(self):
        try:
            for line in self.lrcLines:
                if (line.startswith('[offset:')):
                    line = line.replace(' ', '')
                    offsetMS = line[8:-1]
                    return float(int(offsetMS) / 1000)
        except:
            pass

        return 0

    def __processContent(self):
        d = {}
        for line in self.lrcLines:
            lrcTime, lyrics = self.__processLine(line)

            # secs = self.__convertTime(lrcTime, False)
            secs = self.__convertTime(lrcTime, True)
            
            if (secs != None):
                # Convert it to str() for future updates...
                # Like float as key etc
                secs = f'{secs:.1f}'

                d[secs] = lyrics
        
        return d

    def __processLine(self, line: str):
        """
            Splits out the time & lyrics
        """

        parts = line.split(']')

        time = parts.pop(0)
        # Removes everything in front of the '[' character
        # See issue #7
        time = time.split('[')[-1]

        # The rest of the itesm in parts are just the lyrics
        # Form them back like how we splitted it
        lyrics = ']'.join(parts)
        lyrics = lyrics.strip()

        return time, lyrics

    def __convertTime(self, lyricsTime: str, returnFloat=False):
        parts = lyricsTime.split(":")

        try:
            mins = parts[0]
            secs = parts[-1]

            result = float(secs)
            result += int(mins) * 60
            result += self.offset

            if not (returnFloat):
                # result = int(result)
                result = round(result)
            
            return result
        except:
            return None
