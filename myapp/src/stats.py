import os
import pandas as pd
from collections import Counter, defaultdict


# Load the song data
def load_csv(csv_path):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        raise FileNotFoundError(f"{csv_path} not found.")


def get_total_songs(csv_path):
    df = load_csv(csv_path)
    return len(df)


# Define genre mappings
genre_mapping = {
    'pop (includes country)': ['pop', 'k-pop', 'country', 'j-pop', 'europop', 'mandopop', 'new wave', 'hyperpop',
                               'boy band'],
    'hip hop/r&b': ['hip hop', 'rap', 'trap', 'phonk', 'r&b', 'soul', 'drill', 'crunk', 'soul'],
    'edm/electronic': ['electronic', 'house', 'dubstep', 'trance', 'electro', 'techno', 'rave', 'bass', 'step', 'idm',
                       'hardstyle', 'complextro', 'edm', 'bounce', 'dnb', 'glitch', 'lo-fi', 'synthwave', 'big room',
                       'neurofunk', 'ambient', 'breakbeat', 'garage', 'downtempo', 'intelligent dance music',
                       'moombahton', 'eurodance'],
    'rock': ['rock', 'metal', 'punk', 'alternative', 'alt', 'core', 'emo rock', 'screamo', 'thrash', 'british invasion',
             'merseybeat', 'permanent wave', 'grunge', 'emo punk'],
    'classical/jazz': ['classical', 'orchestral', 'baroque', 'instrumental', 'soundtrack', 'romantic', 'symphony',
                       'jazz', 'blues', 'swing', 'big band', 'ska', 'orchestra', 'concert', 'movie tunes', 'bebop'],
    'alternative/indie': ['alternative', 'indie', 'folk', 'acoustic', 'singer-songwriter', 'alt', 'shoegaze',
                          'midwest emo'],
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


# Calculate average values for other audio features by genre
def calculate_average(feature_dict):
    return {genre: sum(feature_list) / len(feature_list) if feature_list else 0 for genre, feature_list in
            feature_dict.items()}


# Function to calculate statistics
def calculate_song_statistics(df):
    # Count occurrences of genres and artists
    genre_counter = Counter()
    artist_counter = Counter()
    key_counter = Counter()
    bpm_by_genre = defaultdict(list)
    represented_genres = defaultdict(set)
    acousticness_by_genre = defaultdict(list)
    danceability_by_genre = defaultdict(list)
    energy_by_genre = defaultdict(list)
    instrumentalness_by_genre = defaultdict(list)
    liveness_by_genre = defaultdict(list)
    loudness_by_genre = defaultdict(list)
    speechiness_by_genre = defaultdict(list)
    valence_by_genre = defaultdict(list)
    mode_by_genre = defaultdict(lambda: {'major': 0, 'minor': 0})

    for _, row in df.iterrows():
        genres = row['genre'].split('; ')
        artists = row['artists'].split('; ')
        key = row['key']
        bpm = row['bpm']
        acousticness = row['acousticness']
        danceability = row['danceability']
        energy = row['energy']
        instrumentalness = row['instrumentalness']
        liveness = row['liveness']
        loudness = row['loudness']
        speechiness = row['speechiness']
        valence = row['valence']
        mode = row['mode']

        genre_counter.update(genres)
        artist_counter.update(artists)
        key_counter.update([key])

        for genre in genres:
            categories = map_genre_to_broad_category(genre, genre_mapping)
            for category in categories:
                bpm_by_genre[category].append(bpm)
                represented_genres[category].add(genre)
                acousticness_by_genre[category].append(acousticness)
                danceability_by_genre[category].append(danceability)
                energy_by_genre[category].append(energy)
                instrumentalness_by_genre[category].append(instrumentalness)
                liveness_by_genre[category].append(liveness)
                loudness_by_genre[category].append(loudness)
                speechiness_by_genre[category].append(speechiness)
                valence_by_genre[category].append(valence)
                if mode == 1:
                    mode_by_genre[category]['major'] += 1
                else:
                    mode_by_genre[category]['minor'] += 1

    # Calculate average BPM
    average_bpm = df['bpm'].mean()
    std_bpm = df['bpm'].std()

    # Calculate average values by genre
    average_bpm_by_genre = {genre: sum(bpm_list) / len(bpm_list) if bpm_list else 0 for genre, bpm_list in
                            bpm_by_genre.items()}
    std_bpm_by_genre = {genre: pd.Series(bpm_list).std() if bpm_list else 0 for genre, bpm_list in bpm_by_genre.items()}

    average_acousticness_by_genre = calculate_average(acousticness_by_genre)
    average_danceability_by_genre = calculate_average(danceability_by_genre)
    average_energy_by_genre = calculate_average(energy_by_genre)
    average_instrumentalness_by_genre = calculate_average(instrumentalness_by_genre)
    average_liveness_by_genre = calculate_average(liveness_by_genre)
    average_loudness_by_genre = calculate_average(loudness_by_genre)
    average_speechiness_by_genre = calculate_average(speechiness_by_genre)
    average_valence_by_genre = calculate_average(valence_by_genre)

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
        'Top Genres': genre_counter.most_common(100),
        'Top Artists': artist_counter.most_common(100),
        'Common Keys': key_counter.most_common(12),
        'Average BPM': average_bpm,
        'Standard Deviation BPM': std_bpm,
        'Average BPM by Genre': average_bpm_by_genre,
        'Standard Deviation BPM by Genre': std_bpm_by_genre,
        'Represented Genres': represented_genres,
        'Average Acousticness': average_acousticness,
        'Average Danceability': average_danceability,
        'Average Energy': average_energy,
        'Average Instrumentalness': average_instrumentalness,
        'Average Liveness': average_liveness,
        'Average Loudness': average_loudness,
        'Average Speechiness': average_speechiness,
        'Average Valence': average_valence,
        'Major Key Count': major_mode,
        'Minor Key Count': minor_mode,
        'Average Acousticness by Genre': average_acousticness_by_genre,
        'Average Danceability by Genre': average_danceability_by_genre,
        'Average Energy by Genre': average_energy_by_genre,
        'Average Instrumentalness by Genre': average_instrumentalness_by_genre,
        'Average Liveness by Genre': average_liveness_by_genre,
        'Average Loudness by Genre': average_loudness_by_genre,
        'Average Speechiness by Genre': average_speechiness_by_genre,
        'Average Valence by Genre': average_valence_by_genre,
        'Mode by Genre': mode_by_genre,

        'Total Artists': len(artist_counter),
        'Total Genres': len(genre_counter),
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

        f.write("## General Stats\n")
        f.write("| Statistic | Value |\n")
        f.write("| --- | ----- |\n")
        f.write(f"| Total Songs | {total_songs}|\n")
        f.write(f"| Total Artists | {stats['Total Artists']:,} |\n")
        f.write(f"| Total Genres | {stats['Total Genres']:,} |\n")
        f.write("\n")

        f.write("### Genre Category Counts\n")
        f.write("| Category | Number of Unique Genres |\n")
        f.write("| --- | ----- |\n")
        sorted_genres = sorted(stats.get('Represented Genres', {}).items(), key=lambda item: len(item[1]), reverse=True)
        for genre, artists in sorted_genres:
            f.write(f"| {genre} | {len(artists):,} |\n")
        f.write("\n")

        f.write("### Top Genres\n")
        f.write("| Genre | Number of Songs |\n")
        f.write("| --- | ----- |\n")
        for item, count in stats['Top Genres']:
            f.write(f"| {item} | {count} |\n")
        f.write("\n")

        f.write("### Top Artists\n")
        f.write("| Artist | Number of Songs |\n")
        f.write("| --- | ----- |\n")
        for item, count in stats['Top Artists']:
            f.write(f"| {item} | {count} |\n")
        f.write("\n")

        f.write("### Common Keys\n")
        f.write("| Key | Count |\n")
        f.write("| --- | ----- |\n")
        for item, count in sorted(stats['Common Keys'], key=lambda x: x[1], reverse=True):
            readable_key = key_mapping[int(item)]
            f.write(f"| {readable_key} | {count} |\n")
        f.write("\n")

        overall_stats_keys = [
            'Average BPM', 'Standard Deviation BPM', 'Average Acousticness', 'Average Danceability',
            'Average Energy', 'Average Instrumentalness', 'Average Liveness', 'Average Loudness',
            'Average Speechiness', 'Average Valence'
        ]

        genre_stats_keys = {
            'Average BPM': 'Average BPM by Genre',
            'Standard Deviation BPM': 'Standard Deviation BPM by Genre',
            'Average Acousticness': 'Average Acousticness by Genre',
            'Average Danceability': 'Average Danceability by Genre',
            'Average Energy': 'Average Energy by Genre',
            'Average Instrumentalness': 'Average Instrumentalness by Genre',
            'Average Liveness': 'Average Liveness by Genre',
            'Average Loudness': 'Average Loudness by Genre',
            'Average Speechiness': 'Average Speechiness by Genre',
            'Average Valence': 'Average Valence by Genre',
        }

        # Print Overall Averages and Average Values by Genre
        f.write("## Song Statistics\n")
        for overall_key in overall_stats_keys:
            f.write(f"### {overall_key}\n")
            f.write(f"{stats[overall_key]}\n\n")

            genre_key = genre_stats_keys[overall_key]
            if genre_key in stats:
                f.write(f"### {genre_key}\n")
                f.write("| Genre | Average Value |\n")
                f.write("| --- | ----- |\n")
                for genre, avg_value in sorted(stats[genre_key].items(), key=lambda x: x[1], reverse=True):
                    f.write(f"| {genre} | {avg_value} |\n")
                f.write("\n")

        f.write("### Mode Statistics\n")
        f.write(f"#### Total Major: {stats['Major Key Count']}\n")
        f.write(f"#### Total Minor: {stats['Minor Key Count']}\n\n")

        f.write("### Mode by Genre\n")
        f.write("| Genre | Major | Minor | Ratio (Major:Minor) |\n")
        f.write("| --- | ----- | ----- | ----- |\n")
        sorted_modes = sorted(stats['Mode by Genre'].items(),
                              key=lambda x: (x[1]['major'] / x[1]['minor']) if x[1]['minor'] != 0 else float('inf'),
                              reverse=True)
        for genre, mode_counts in sorted_modes:
            major = mode_counts['major']
            minor = mode_counts['minor']
            ratio = f"{major / minor}" if minor != 0 else "∞"
            f.write(f"| {genre} | {major} | {minor} | {ratio} |\n")
        f.write("\n")

        # Print Represented Genres
        f.write("### Represented Genres\n")
        f.write("| Category | Represented Genres |\n")
        f.write("| --- | ----- |\n")
        for category, genres in sorted(stats['Represented Genres'].items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"| {category} | {', '.join(genres)} |\n")
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

    # Get top 100 artists by category
    for category in top_artists_by_category:
        top_artists_by_category[category].sort(key=lambda x: x['followers'], reverse=True)
        top_artists_by_category[category] = top_artists_by_category[category][:100]

    # Prepare the statistics dictionary
    stats = {
        'Top Genres': genre_counter.most_common(100),
        'Number of Artists by Category': category_artist_counter,
        'Top Artists by Category': top_artists_by_category,
        'All Artists by Category': all_artists_by_category,
        'Total Artists': len(processed_artists),
        'Total Genres': len(genre_counter),
    }

    return stats


# Save artist statistics to Markdown File
def save_artist_statistics(stats, file_path):
    with open(file_path, 'w') as f:
        f.write("# Artist Stats\n\n")

        f.write("## General Stats\n")
        f.write("| Statistic | Value |\n")
        f.write("| --- | ----- |\n")
        f.write(f"| Total Artists | {stats['Total Artists']:,} |\n")
        f.write(f"| Total Genres | {stats['Total Genres']:,} |\n")

        # Top Genres
        f.write("### Top 100 Genres\n")
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
            f.write(f"### Top 100 Artists for {category}\n")
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
    choice = input("1) Song Statistics\n2) Artist Statistics\nChoose an option: ")

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
    total_songs = get_total_songs('../data/songs_data.csv')
    main()
