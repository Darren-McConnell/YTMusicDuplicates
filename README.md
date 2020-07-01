# YTMusicDuplicates

## Requirements

- Python 3.6 or higher

## Setup

Clone repo & install third party requirements:
- `git clone https://github.com/Darren-McConnell/lbxd_slack_bot.git` 
- `pip3 install -r requirements.txt`

Set authenticated request headers: 
- Follow the [__ytmusicapi docs__](https://ytmusicapi.readthedocs.io/en/latest/setup.html#authenticated-requests) to update the cookie value in `headers_auth.json`

## Usage
```
remove_dupes.py [-h] (--all_playlists | --playlist PLAYLIST)

optional arguments:
  -h, --help           show this help message and exit
  --all_playlists      Remove duplicates from all user playlists
  --playlist PLAYLIST  Remove duplicates from single specified playlist
  ```
