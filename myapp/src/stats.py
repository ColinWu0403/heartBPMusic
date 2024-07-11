import os
import pandas as pd
from collections import Counter, defaultdict

# Load the song data
def load_csv(csv_path):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        raise FileNotFoundError(f"{csv_path} not found.")

# Define genre mappings
genre_mapping = {
    'pop (includes country)': ['pop', 'country'],
    'hip hop/r&b': ['hip hop', 'rap', 'trap', 'phonk', 'r&b', 'soul', 'drill'],
    'edm/electronic': ['electronic', 'house', 'dubstep', 'trance', 'electro', 'techno', 'rave', 'bass', 'step', 'idm', 'hardstyle', 'complextro', 'edm', 'bounce', 'dnb', 'glitch', 'lo-fi', 'synthwave', 'big room', 'neurofunk', 'ambient'],
    'rock': ['rock', 'metal', 'punk', 'alternative', 'alt', 'core', 'emo rock', 'screamo', 'thrash', 'british invasion', 'merseybeat', 'permanent wave', 'grunge', 'emo punk'],
    'classical/jazz': ['classical', 'orchestral', 'baroque', 'instrumental', 'romantic', 'symphony', 'jazz', 'blues', 'swing', 'big band', 'ska'],
    'alternative/indie': ['alternative', 'indie', 'folk', 'acoustic', 'singer-songwriter', 'alt'],
    'others': []  # To handle genres that don't fit into the above categories
}

def map_genre_to_broad_category(genre, genre_mapping):
    categories = []
    for broad_category, specific_genres in genre_mapping.items():
        if any(specific_genre in genre.lower() for specific_genre in specific_genres):
            categories.append(broad_category)
    if not categories:
        categories.append('others')
    return categories

# Function to calculate statistics
def calculate_song_statistics(df):
    # Count occurrences of genres and artists
    genre_counter = Counter()
    artist_counter = Counter()
    key_counter = Counter()
    bpm_by_genre = defaultdict(list)
    represented_genres = defaultdict(set)

    for _, row in df.iterrows():
        genres = row['genre'].split('; ')
        artists = row['artists'].split('; ')
        key = row['key']
        bpm = row['bpm']
        
        genre_counter.update(genres)
        artist_counter.update(artists)
        key_counter.update([key])
        
        for genre in genres:
            categories = map_genre_to_broad_category(genre, genre_mapping)
            for category in categories:
                bpm_by_genre[category].append(bpm)
                represented_genres[category].add(genre)

    # Calculate average BPM
    average_bpm = df['bpm'].mean()
    std_bpm = df['bpm'].std()
    
    # Calculate average BPM by genre
    average_bpm_by_genre = {genre: sum(bpm_list) / len(bpm_list) if bpm_list else 0 for genre, bpm_list in bpm_by_genre.items()}
    
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
        'Average BPM by Genre': average_bpm_by_genre,
        'Represented Genres': represented_genres,
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

# Save song statistics to Markdown File
def save_song_statistics(stats, file_path):
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
            elif key == 'Average BPM by Genre':
                f.write("| Genre | Average BPM |\n")
                f.write("| --- | ----- |\n")
                for genre, avg_bpm in value.items():
                    f.write(f"| {genre} | {avg_bpm} |\n")
            elif key == 'Represented Genres':
                f.write("| Category | Represented Genres |\n")
                f.write("| --- | ----- |\n")
                for category, genres in value.items():
                    f.write(f"| {category} | {', '.join(genres)} |\n")
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

# Function to calculate artist statistics
def calculate_artist_statistics(df):
    # Count occurrences of genres and artists
    genre_counter = Counter()
    category_artist_counter = Counter()
    top_artists_by_category = defaultdict(list)
    all_artists_by_category = defaultdict(set)
    processed_artists = set()
    
    for _, row in df.iterrows():
        artist_name = row['name']
        if artist_name in processed_artists:
            continue
        processed_artists.add(artist_name)
        
        followers = row['followers']
        popularity = row['popularity']
        genres = row['genres'].strip('"').split(', ')
        
        artist_data = {'name': artist_name, 'followers': followers, 'popularity': popularity}

        artist_categories = set()
        for genre in genres:
            genre_counter[genre] += 1
            categories = map_genre_to_broad_category(genre, genre_mapping)
            artist_categories.update(categories)
        
        for category in artist_categories:
            category_artist_counter[category] += 1
            top_artists_by_category[category].append(artist_data)
            all_artists_by_category[category].add(artist_name)
    
    # Convert sets back to lists
    all_artists_by_category = {k: list(v) for k, v in all_artists_by_category.items()}

    # Get top 25 artists by category
    for category in top_artists_by_category:
        top_artists_by_category[category].sort(key=lambda x: x['followers'], reverse=True)
        top_artists_by_category[category] = top_artists_by_category[category][:25]

    # Prepare the statistics dictionary
    stats = {
        'Top Genres': genre_counter.most_common(50),
        'Number of Artists by Category': category_artist_counter,
        'Top Artists by Category': top_artists_by_category,
        'All Artists by Category': all_artists_by_category
    }

    return stats

# Save artist statistics to Markdown File
def save_artist_statistics(stats, file_path):
    with open(file_path, 'w') as f:
        f.write("# Artist Stats\n\n")

        # Top Genres
        f.write("### Top Genres\n")
        f.write("| Genre | Number of Artists |\n")
        f.write("| --- | ----- |\n")
        for genre, count in stats['Top Genres']:
            f.write(f"| {genre} | {count:,} |\n")
        f.write("\n")

        # Number of Artists by Category
        f.write("### Number of Artists by Category\n")
        f.write("| Category | Number of Artists |\n")
        f.write("| --- | ----- |\n")
        for category, count in stats['Number of Artists by Category'].items():
            f.write(f"| {category} | {count:,} |\n")
        f.write("\n")

        # Top Artists by Category
        for category, artists in stats['Top Artists by Category'].items():
            f.write(f"### Top Artists for {category}\n")
            f.write("| Artist Name | Followers | Popularity |\n")
            f.write("| --- | ----- | ----- |\n")
            for artist in artists:
                f.write(f"| {artist['name']} | {artist['followers']:,} | {artist['popularity']} |\n")
            f.write("\n")

        # All Artists by Category
        f.write("### All Artists by Category\n")
        f.write("| Category | All Artists |\n")
        f.write("| --- | ----- |\n")
        for category, artists in stats['All Artists by Category'].items():
            f.write(f"| {category} | {', '.join(artists)} |\n")
        f.write("\n")

def main():
    choice = input("Choose between Song Statistics or Artist Statistics: ")
    
    if choice == '1':
        print("Song Statistics")
        
        # Paths to files
        songs_csv_path = os.path.join(os.path.dirname(__file__), '../data/songs_data.csv')
        stats_md_path = os.path.join(os.path.dirname(__file__), '../data/song_stats.md')

        # Load song data
        song_df = load_csv(songs_csv_path)

        # Calculate statistics
        song_stats = calculate_song_statistics(song_df)

        # Save statistics to markdown file
        save_song_statistics(song_stats, stats_md_path)
    elif choice == '2':
        print("Artist Statistics")
        
        # Paths to files
        artists_csv_path = os.path.join(os.path.dirname(__file__), '../data/artists_data.csv')
        stats_md_path = os.path.join(os.path.dirname(__file__), '../data/artist_stats.md')

        # Load artist data
        artist_df = load_csv(artists_csv_path)

        # Calculate statistics
        artist_stats = calculate_artist_statistics(artist_df)

        # Save statistics to markdown file
        save_artist_statistics(artist_stats, stats_md_path)
    else:
        print("Invalid choice. Please choose 1 or 2.")
    
if __name__ == "__main__":
    main()