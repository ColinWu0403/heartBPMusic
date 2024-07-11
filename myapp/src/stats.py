import os
import pandas as pd
from collections import Counter

# Load the song data
def load_song_data(csv_path):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        raise FileNotFoundError(f"{csv_path} not found.")

# Function to calculate statistics
def calculate_statistics(df):
    # Count occurrences of genres and artists
    genre_counter = Counter()
    artist_counter = Counter()
    key_counter = Counter()

    for _, row in df.iterrows():
        genres = row['genre'].split('; ')
        artists = row['artists'].split('; ')
        key = row['key']

        genre_counter.update(genres)
        artist_counter.update(artists)
        key_counter.update([key])

    # Calculate average BPM
    average_bpm = df['bpm'].mean()
    std_bpm = df['bpm'].std()
    
    # Calculate average values for other audio features
    average_acousticness = df['acousticness'].mean()
    average_danceability = df['danceability'].mean()
    average_energy = df['energy'].mean()
    average_instrumentalness = df['instrumentalness'].mean()
    average_liveness = df['liveness'].mean()
    average_loudness = df['loudness'].mean()
    average_speechiness = df['speechiness'].mean()
    average_valence = df['valence'].mean()
    major_mode = df['mode'].value_counts().get(1, 0)
    minor_mode = df['mode'].value_counts().get(0, 0)
        
    # Prepare the statistics dictionary
    stats = {
        'Top Genres': genre_counter.most_common(50),
        'Top Artists': artist_counter.most_common(50),
        'Common Keys': key_counter.most_common(12),
        'Average BPM': average_bpm,
        'Standard Deviation BPM': std_bpm,
        'Average Acousticness': average_acousticness,
        'Average Danceability': average_danceability,
        'Average Energy': average_energy,
        'Average Instrumentalness': average_instrumentalness,
        'Average Liveness': average_liveness,
        'Average Loudness': average_loudness,
        'Average Speechiness': average_speechiness,
        'Average Valence': average_valence,
        'Major Key Count': major_mode,
        'Minor Key Count': minor_mode
    }
    
    return stats

# Function to save statistics to Markdown File
def save_statistics_to_md(stats, file_path):
    key_mapping = {
        -1: "No Key",
        0: "C",
        1: "C♯/D♭",
        2: "D",
        3: "D♯/E♭",
        4: "E",
        5: "F",
        6: "F♯/G♭",
        7: "G",
        8: "G♯/A♭",
        9: "A",
        10: "A♯/B♭",
        11: "B"
    }
    
    with open(file_path, 'w') as f:
        f.write("# Song Stats\n\n")
        for key, value in stats.items():
            f.write(f"### {key}\n")
            if key == 'Common Keys':
                f.write("| Key | Count |\n")
                f.write("| --- | ----- |\n")
                for item, count in value:
                    readable_key = key_mapping[int(item)]
                    f.write(f"| {readable_key} | {count} |\n")
            elif isinstance(value, list):
                if key == 'Top Genres':
                    f.write("| Genre | Count |\n")
                    f.write("| --- | ----- |\n")
                elif key == 'Top Artists':
                    f.write("| Artist | Count |\n")
                    f.write("| --- | ----- |\n")
                for item, count in value:
                    f.write(f"| {item} | {count} |\n")
            else:
                f.write(f"{value}\n")
            f.write("\n")

# Paths to CSV files
songs_csv_path = os.path.join(os.path.dirname(__file__), '../data/songs_data.csv')
stats_md_path = os.path.join(os.path.dirname(__file__), '../data/song_stats.md')

# Load song data
song_df = load_song_data(songs_csv_path)

# Calculate statistics
song_stats = calculate_statistics(song_df)

# Save statistics to markdown file
save_statistics_to_md(song_stats, stats_md_path)
