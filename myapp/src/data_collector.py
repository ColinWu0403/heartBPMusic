import os
import time
import pandas as pd
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# Spotify API credentials
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Function to get tracks for an artist
def get_tracks_for_artist(artist_id):
    results = sp.artist_top_tracks(artist_id)
    tracks = results['tracks']
    return tracks

# Function to get audio features for a track
def get_audio_features(track_id):
    audio_features = sp.audio_features([track_id])[0]
    return audio_features

def collect_data(artist_ids):
    # Collect data
    songs_data = []

    for artist_id in artist_ids:
        tracks = get_tracks_for_artist(artist_id)
        for track in tracks:
            track_id = track['id']
            track_name = track['name']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            audio_features = get_audio_features(track_id)

            if audio_features:  # Only proceed if audio features are available
                song_data = {
                    'name': track_name,
                    'creators': artists,
                    'bpm': audio_features['tempo'],
                    'genre': ', '.join(sp.artist(artist_id)['genres']),
                    'key': audio_features['key'],
                    'danceability': audio_features['danceability'],
                    'energy': audio_features['energy'],
                    'instrumentalness': audio_features['instrumentalness'],
                    'liveness': audio_features['liveness'],
                    'loudness': audio_features['loudness'],
                    'speechiness': audio_features['speechiness'],
                    'mode': audio_features['mode'],
                    'valence': audio_features['valence']
                }
                songs_data.append(song_data)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(songs_data)
    df.to_csv('songs_metadata.csv', index=False)

    return df
