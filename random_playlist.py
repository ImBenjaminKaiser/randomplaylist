import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Spotify API credentials
CLIENT_ID = 'CLIENT_ID_HERE'
CLIENT_SECRET = 'CLIENT_SECRET_HERE'
REDIRECT_URI = 'REDIRECT_URI_HERE'  # Must match the one set in your Spotify app settings
SCOPE = 'playlist-modify-public playlist-modify-private'
  # Scope allowing to modify user's public playlists

# Playlist ID (the last part of your playlist's Spotify URI)
PLAYLIST_ID = 'YOUR_PLAYLIST_ID_HERE'

# Initialize the Spotipy client with SpotifyOAuth for user authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

def makeid(length):
    """Generate a random string of given length."""
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(characters) for i in range(length))

def find_random_songs(num_songs=900):
    """Find and return URIs of random songs."""
    song_uris = []
    while len(song_uris) < num_songs:
        random_query = makeid(2)
        results = sp.search(q=random_query, type='track', limit=50)  # Fetch fewer if API limits are reached
        tracks = results['tracks']['items']
        for track in tracks:
            if len(song_uris) < num_songs:
                song_uris.append(track['uri'])
            else:
                break
    return song_uris

def add_songs_to_playlist(playlist_id, song_uris):
    """Add songs to a specific playlist given by playlist_id."""
    sp.playlist_add_items(playlist_id, song_uris)
    print(f"Added {len(song_uris)} songs to the playlist {playlist_id}")

# Main
random_songs_uris = find_random_songs()
add_songs_to_playlist(PLAYLIST_ID, random_songs_uris)
