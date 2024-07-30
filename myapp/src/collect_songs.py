import os
import time
import pandas as pd
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from stats import genre_mapping, map_genre_to_broad_category
from search_artists import get_specific_genres

def load_artist_data(csv_path, artists_to_exclude):
    if os.path.exists(csv_path):
        artist_df = pd.read_csv(csv_path)
        filtered_artist_df = artist_df[~artist_df['id'].isin(artists_to_exclude)]
        return filtered_artist_df
    else:
        raise FileNotFoundError(f"{csv_path} not found.")

def select_random_artist(artist_df):
    return artist_df.sample(n=1).iloc[0]

def select_random_artists(artist_df, num_artists=20):
    return artist_df.sample(n=num_artists)

def get_audio_features(track_ids):
    audio_features = sp.audio_features(track_ids)
    return audio_features

def load_existing_data(csv_path):
    if os.path.exists(csv_path):
        try:
            df_existing = pd.read_csv(csv_path)
            artist_counts = df_existing['artists'].value_counts()
            artists_to_exclude = artist_counts[artist_counts >= 10].index.tolist()
            return df_existing, artists_to_exclude
        except pd.errors.EmptyDataError:
            # If the file is empty, create an empty DataFrame with the required columns
            return pd.DataFrame(columns=[
                'name', 'artists', 'id', 'bpm', 'genre', 'key', 'acousticness',
                'danceability', 'energy', 'instrumentalness', 'liveness',
                'loudness', 'speechiness', 'mode', 'valence', 'href', 'uri'
            ]), []
    else:
        return pd.DataFrame(), []

def get_audio_features(track_ids):
    audio_features = sp.audio_features(track_ids)
    return audio_features

# Collects all features using the Spotify API to create a DataFrame
def collect_song_data(artist_ids):
    # Collect data
    songs_data = []

    # Get top tracks for each artist
    for artist_id in artist_ids:
        results = sp.artist_top_tracks(artist_id)
        tracks = results['tracks']
        
        for track in tracks:
            track_id = track['id']
            track_name = track['name']
            artists = '; '.join([artist['name'] for artist in track['artists']])
            
            # Fetch additional details including genres and original artists
            audio_features = sp.audio_features([track_id])[0]  # Fetch audio features for the track
            
            if audio_features:  # Only proceed if audio features are available
                
                song_data = {
                    'name': track_name,
                    'artists': artists,
                    'id': track_id,
                    'bpm': audio_features['tempo'],
                    'genre': '; '.join(sp.artist(artist_id)['genres']),
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

            time.sleep(0.5)  # Add a delay to respect rate limits

    df = pd.DataFrame(songs_data)
    return df

def append_to_csv(df, csv_path, df_existing):
    df_combined = pd.concat([df_existing, df], ignore_index=True)
    df_combined.to_csv(csv_path, index=False)

def main():
    # Paths to CSV files
    artist_csv_path = '../static/data/artists_data.csv'
    songs_csv_path = '../static/data/songs_data.csv'

    # Load existing song data and get artists to exclude
    df_existing, artists_to_exclude = load_existing_data(songs_csv_path)

    # Load artist data excluding artists to exclude
    artist_df = load_artist_data(artist_csv_path, artists_to_exclude)
    
    option = input("Choose an option:\n1. Random Song Collection\n2. Collect by Genre Category\nEnter your choice (1 or 2): ")
    if option == '1':
        choice = input("1) Collect Batch of Songs\n2) Collect Single Artist Top Songs\nEnter Choice: ")

        if choice == '1':
            print("Collecting top songs for a batch of artists...")

            # Select a fixed number of random artists
            selected_artists = select_random_artists(artist_df, num_artists=50)
            selected_artist_ids = selected_artists['id'].tolist()

            # Collect song data for the selected artists
            new_song_data = collect_song_data(selected_artist_ids)

            # Append new song data to CSV
            append_to_csv(new_song_data, songs_csv_path, df_existing)
        elif choice == '2':
            print("Collecting top songs for a single artist...")

            # Select one random artist
            selected_artist = select_random_artist(artist_df)
            selected_artist_id = selected_artist['id']

            # Collect song data for the selected artist
            new_song_data = collect_song_data([selected_artist_id])

            # Append new song data to CSV
            append_to_csv(new_song_data, songs_csv_path, df_existing)
    elif option == '2':
        print("Collecting top songs by genre category...")
        print("Available genres:")
        print("1. Pop")
        print("2. Hip Hop/r&b")
        print("3. Rock")
        print("4. EDM/Electronic")
        print("5. Classical/Jazz")
        print("6. Alternative/Indie")
        print("7. Other")
        
        genre_choice = input("Enter genre (1-7): ")
        genre_map = {
            "1": "pop (includes country)",
            "2": "hip hop/r&b",
            "3": "rock",
            "4": "edm/electronic",
            "5": "classical/jazz",
            "6": "alternative/indie",
            "7": "others"
        }
        
        broad_genre = genre_map.get(genre_choice)
        if not broad_genre:
            print("Invalid genre choice.")
            return
        
        # Get specific genres for the selected broad genre
        specific_genres = get_specific_genres(broad_genre, genre_mapping)
        
        print(specific_genres)
        
        # Filter the artist dataframe for the selected specific genres
        filtered_artists_df = artist_df[artist_df['genres'].apply(lambda genres: any(specific_genre in genres for specific_genre in specific_genres))]
        
        # Select a fixed number of random artists from the filtered dataframe
        selected_artists = select_random_artists(filtered_artists_df, num_artists=30)
        selected_artist_ids = selected_artists['id'].tolist()

        print(selected_artists[['name', 'genres']])
        
        # Collect song data for the selected artists
        new_song_data = collect_song_data(selected_artist_ids)

        # Append new song data to CSV
        append_to_csv(new_song_data, songs_csv_path, df_existing)

    else:
        print("Invalid choice. Exiting...")
        return

if __name__ == "__main__":
    # Load environment variables from .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(dotenv_path)

    # Spotify API credentials
    CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

    # Authenticate with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

    main()