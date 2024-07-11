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

def load_artist_data(csv_path):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        raise FileNotFoundError(f"{csv_path} not found.")

def select_random_artists(artist_df, num_artists=20):
    return artist_df.sample(n=num_artists)

def load_existing_data(csv_path):
    if os.path.exists(csv_path):
        try:
            return pd.read_csv(csv_path)
        except pd.errors.EmptyDataError:
            # If the file is empty, create an empty DataFrame with the required columns
            return pd.DataFrame(columns=[
                'name', 'artists', 'id', 'bpm', 'genre', 'key', 'acousticness',
                'danceability', 'energy', 'instrumentalness', 'liveness',
                'loudness', 'speechiness', 'mode', 'valence', 'href', 'uri'
            ])
    else:
        return pd.DataFrame()

def get_tracks_for_artist(artist_id):
    results = sp.artist_top_tracks(artist_id)
    tracks = results['tracks']
    return tracks

def get_audio_features(track_ids):
    audio_features = sp.audio_features(track_ids)
    return audio_features

# Collects all features using the Spotify API to create a DataFrame
def collect_song_data(artist_ids):
    # Collect data
    songs_data = []

    for artist_id in artist_ids:
        tracks = get_tracks_for_artist(artist_id)
        track_ids = [track['id'] for track in tracks]
        track_names = [track['name'] for track in tracks]
        track_artists = ['; '.join([artist['name'] for artist in track['artists']]) for track in tracks]
        genres = '; '.join(sp.artist(artist_id)['genres'])

        # Split track_ids into batches of 100
        for i in range(0, len(track_ids), 100):
            batch_track_ids = track_ids[i:i + 100]
            batch_track_names = track_names[i:i + 100]
            batch_track_artists = track_artists[i:i + 100]

            audio_features_list = get_audio_features(batch_track_ids)

            for j, audio_features in enumerate(audio_features_list):
                if audio_features:  # Only proceed if audio features are available
                    song_data = {
                        'name': batch_track_names[j],
                        'artists': batch_track_artists[j],
                        'id': batch_track_ids[j],
                        'bpm': audio_features['tempo'],
                        'genre': genres,
                        'key': audio_features['key'],
                        'acousticness': audio_features['acousticness'],
                        'danceability': audio_features['danceability'],
                        'energy': audio_features['energy'],
                        'instrumentalness': audio_features['instrumentalness'],
                        'liveness': audio_features['liveness'],
                        'loudness': audio_features['loudness'],
                        'speechiness': audio_features['speechiness'],
                        'mode': audio_features['mode'],
                        'valence': audio_features['valence'],
                        'href': audio_features['track_href'],
                        'uri': audio_features['uri'],
                    }
                    songs_data.append(song_data)

    df = pd.DataFrame(songs_data)
    return df

def append_to_csv(df, csv_path):
    df_existing = load_existing_data(csv_path)
    df_combined = pd.concat([df_existing, df], ignore_index=True)
    df_combined.to_csv(csv_path, index=False)

# Paths to CSV files
artist_csv_path = os.path.join(os.path.dirname(__file__), '../data/artists_data.csv')
songs_csv_path = os.path.join(os.path.dirname(__file__), '../data/songs_data.csv')

# Load artist data
artist_df = load_artist_data(artist_csv_path)

# Select a fixed number of random artists
selected_artists = select_random_artists(artist_df, num_artists=20)
selected_artist_ids = selected_artists['id'].tolist()

# Collect song data for the selected artists
new_song_data = collect_song_data(selected_artist_ids)

# Append new song data to CSV
append_to_csv(new_song_data, songs_csv_path)