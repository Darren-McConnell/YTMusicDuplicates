import argparse

from ytmusicapi import YTMusic


SONG_LIMIT = 5000
PLAYLIST_LIMIT = 10000

ytmusic = YTMusic('headers_auth.json')


def parse_song_title(artist_list, song_title):
    if len(artist_list) == 1:
        artists_str = artist_list[0]
    else:
        artists_str = f'{", ".join(artist_list[:-1])} & {artist_list[-1]}'

    return f'Artist: {artists_str} --- Song: {song_title}'


def parse_duplicates(track_list):
    keep_list = set()
    dupe_list = []
    for track in track_list:
        videoId = track['videoId']
        artists = [a['name'] for a in track['artists']]
        title = parse_song_title(artists, track['title'])
        if videoId in keep_list:
            if 'setVideoId' not in track.keys():
                continue
            dupe_list.append({'title': title,
                              'videoId': videoId,
                              'setVideoId': track['setVideoId']})
        else:
            keep_list.add(videoId)
    return dupe_list


def get_playlist_dupes(pl_id, pl_title):
    print(f'Dupe checking "{pl_title}" ...')
    playlist = ytmusic.get_playlist(pl_id, SONG_LIMIT)
    dupe_list = parse_duplicates(playlist['tracks'])
    if dupe_list:
        dupes_str = '\n\t'.join(set([d['title'] for d in dupe_list]))
        print(f'{len(dupe_list)} duplicate songs from "{pl_title}" '
              f'found. Unique items with duplicates:\n\t{dupes_str}\n')
    
    return dupe_list


def continue_check(prompt):
    while True:
        response = input(f'\n{prompt} y or n: ')
        if response.lower() not in 'yn':
            print('Invalid response!')
            continue
        break
    
    if response.lower() == 'n':
        print('Quitting...')
        quit()
        

def parse_cmdline_args():
    parser = argparse.ArgumentParser(description='')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all_playlists', action='store_true',
                       help='Remove duplicates from all user playlists')
    group.add_argument('--playlist', 
                       help='Remove duplicates from single specified playlist')
    return parser.parse_args()


def main():
    args = parse_cmdline_args()

    playlists = ytmusic.get_library_playlists(PLAYLIST_LIMIT)

    if not args.all_playlists:
        playlists = [pl  for pl in playlists if pl['title'] == args.playlist]
        if len(playlists) == 0:
            print(f'No playlist called "{args.playlist}" was found')
            quit()
        elif len(playlists) > 1:
            continue_check(f'More than 1 playlist "{args.playlist}" found. '
                           'Continue and remove duplicates in all instances?')   
    
    duplicates = []
    for pl in playlists:
        pl_dupe_list = get_playlist_dupes(pl['playlistId'], pl['title'])
        if pl_dupe_list:
            duplicates.append((pl['playlistId'], pl['title'], pl_dupe_list))

    if duplicates:
        continue_check('Are you sure you want to delete the above duplicates?')

        for pl_id, pl_title, dupe in duplicates:
            print(f'Removing duplicates from {pl_title}...')
            ytmusic.remove_playlist_items(pl_id, dupe)
        print(f'\nAll duplicates deleted successfully!')
    else:
        print('\nNo duplicates found!')

if __name__ == '__main__':
    main()