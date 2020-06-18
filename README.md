# tf2-voice-ban-bots
This is a Python script designed for Team Fortress 2 that will pull a list of known bots from [Pazer's TF2 Bot Detector](https://github.com/PazerOP/tf2_bot_detector/), my own list of bots, and [wgetJane's list of bots](https://gist.github.com/wgetJane/0bc01bd46d7695362253c5a2fa49f2e9/), and write their Steam IDs to a voice_ban.dt file.

Essentially what this allows for is the replacement of a user's current voice_ban.dt file, which is used to store a list of muted players. This will effectively mute most, if not all, known bots in-game, preventing them from spamming chat/voice chat.

Using this tool will not give you a VAC ban, nor should editing the list of muted players in your TF2 directory.

## How to use
Run the `tf2_voice_ban_bots.py` file. `py -3 tf2_voice_ban_bots.py`

It will grab the list of bots and generate a voice_ban.dt file if you wish to do so.

## Requirements
Python 3.x or later

'requests' Python module
