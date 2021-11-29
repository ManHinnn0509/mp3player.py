# mp3player.py
MP3 Player with Tkinter and Pygame in Python

**This is created for fun.** Also because all the .mp3 players I have has the same issue, high CPU and RAM usage.

So I decided to create my own so that I can listen to music while I'm gaming without lag

P.S: **I'm not professional with Tkinter / Pygame.**

## Requirements

See [requirements.txt](./requirements.txt)

## To start the player

Actually just run the `main.py` or `v1/main_v1.py` will do the job

I added `.bat` file for quick restart which debugging / developing

## Planned

* [x] [Add time control (Time slider?)](https://github.com/ManHinnn0509/mp3player.py/commit/6ec3a412478984309697aeb6518540c91b4c5288)
* [ ] Add lyrics display (Maybe LRC File? [維基][zh_wiki_lrc] / [wiki][en_wiki_lrc])
* [x] Add more comment for the codes (Added in current version)
* [x] **Rework with better and clearer code** (Moved old codes into [`v1`](./v1) dir)

## Known issues

* Might unable to load some .mp3 files (Due to encoding issue?)
* See [Issues][issues]

[issues]: https://github.com/ManHinnn0509/mp3player.py/issues

[zh_wiki_lrc]: https://zh.wikipedia.org/wiki/LRC%E6%A0%BC%E5%BC%8F
[en_wiki_lrc]: https://en.wikipedia.org/wiki/LRC_%28file_format%29