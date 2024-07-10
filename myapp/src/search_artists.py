import os
import time
import json
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

# Function to search for artists by genre within a follower range
def search_artists_by_genre(genre, min_followers, max_followers):
    artists_data = []
    results = sp.search(q=f'genre:"{genre}"', type='artist', limit=50)
    artists = results['artists']['items']
    for artist in artists:
        followers = artist['followers']['total']
        if min_followers <= followers <= max_followers:
            artist_data = {
                'name': artist['name'],
                'id': artist['id'],
                'genres': ', '.join(artist['genres']),
                'followers': followers,
                'popularity': artist['popularity'],
                'spotify_url': artist['external_urls']['spotify']
            }
            artists_data.append(artist_data)
    return artists_data

# Function to get random artists from a list of genres and follower ranges
def get_random_artists(genres, follower_ranges, num_artists=100):
    min_followers, max_followers = random.choice(follower_ranges)
    artists_data = []
    for genre in genres:
        random_artists = search_artists_by_genre(genre, min_followers, max_followers)
        artists_data.extend(random_artists)
    random.shuffle(artists_data)
    return artists_data[:num_artists]

# Function to load genres from JSON file
def load_genres_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        genres_data = json.load(f)
    return [genre['name'] for genre in genres_data]  # Extracting just the genre names
  
# Function to load existing data from CSV
def load_existing_data(csv_path):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame()

# Define follower ranges
follower_ranges = [
    (5000, 50000), # 5k to 50k
    (50000, 250000), # 50k to 250k
    (250000, 1000000), # 250k to 1 mill
    (1000000, 5000000), # 1 mill to 5 mill
    (5000000, 100000000) # 5 mill to Max (100 mill)
]

json_file_path = os.path.join(os.path.dirname(__file__), '../data/spotify_genres.json')

# Load genres from JSON file
genres = load_genres_from_file(json_file_path)

print("Searching for random artists...")

# Collecting data
artists_data = get_random_artists(genres, follower_ranges)

# Convert to DataFrame
df_new = pd.DataFrame(artists_data)

# Load existing data from CSV
csv_path = os.path.join(os.path.dirname(__file__), '../data/artists_data.csv')
df_existing = load_existing_data(csv_path)

# Append new data to existing DataFrame
df_combined = pd.concat([df_existing, df_new], ignore_index=True)

# Save to CSV (overwrite mode)
df_combined.to_csv(csv_path, index=False)

print(f"Data collection complete. Saved to '{csv_path}'")