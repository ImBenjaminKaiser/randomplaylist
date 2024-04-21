import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import os
import sys
import time
from win10toast import ToastNotifier
from langdetect import detect
import lyricsgenius


user_set_num_songs = 100 # Number of songs to add to the playlist
remove_previous_songs = False  # If True, removes all songs from the playlist before adding new ones

desired_language = "en"  # Language of the songs you want to add to the playlist

toast = ToastNotifier()

client_access_token = ""
LyricsGenius = lyricsgenius.Genius(client_access_token)


# Spotify API credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:8888/callback'  # Must match the one set in your Spotify app settings
SCOPE = 'playlist-modify-public playlist-modify-private'
# Scope allowing to modify user's public and private playlists

# Playlist ID (the last part of the  playlist's Spotify URI)
PLAYLIST_ID = ''

# Get user credentials access token
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# https://stackoverflow.com/a/52011313
def progressBar(name, value, endvalue, bar_length = 50, width = 20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent*bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write("\r{0: <{1}} : [{2}]{3}% \n".format(\
                    name, width, arrow + spaces, int(round(percent*100))))
    sys.stdout.flush()
    if value == endvalue:
        sys.stdout.write('\n\n')

def makeid(length):
    # Generate a random string of given length (1-3)
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(characters) for i in range(length))

def find_random_songs(num_songs=user_set_num_songs):
    #Find and return URIs of random songs.

    song_uris = []

    for i in range(num_songs):

        # Pick 1-3 characters from list above and assign them to random_query
        random_query = makeid(random.randint(1,3))

        # Add wildcard operator to search
        wild_card = random.randint(1, 3)
        if wild_card == 1:
            random_query = random_query + "%"
        elif wild_card == 2:
            random_query = "%" + random_query
        elif wild_card == 3:
            random_query = "%" + random_query + "%"

        # Like picking the page number
        offset_amount = random.randint(0, 999)

        # Search spotify API, returns english one song in JSON
        results = sp.search(q=random_query, limit=1, offset=offset_amount, type='track')
        try:
            # Check if 'items' key exists in the results['tracks'] dictionary
                artist_name = results['tracks']['items'][0]['artists'][0]['name']
                song_name = results['tracks']['items'][0]['name']
                print("Waiting")
                time.sleep(5)
                song = LyricsGenius.search_song(song_name, artist_name)
                if song != None:
                    language = detect(song.lyrics)
                    if language == desired_language:
                        tracks = results['tracks']['items']

                        for track in tracks:
                            if len(song_uris) < num_songs:
                                song_uris.append(track['uri'])
                                add_songs_to_playlist(PLAYLIST_ID, song_uris)
                                print("Song added to playlist")
                                song_uris = []

                            else:
                                break
                    else:
                        print("Song not in desired language")
                        continue
                else:
                    continue


        except IndexError:
            # Ignore or handle the case when there are no items
            continue

    time.sleep(0.1)
    if song_uris:
        return song_uris
    else:
        return



def add_songs_to_playlist(playlist_id, song_uris):
    sp.playlist_add_items(playlist_id, song_uris)


# Main
if (remove_previous_songs == True):
    sp.playlist_remove_all_occurrences_of_items(PLAYLIST_ID, [])
    print("Removed all songs from the playlist")

for i in range(10):
    find_random_songs()
