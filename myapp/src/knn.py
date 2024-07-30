import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import os
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from .stats import genre_mapping


def load_data(file_path):
    return pd.read_csv(file_path)


def map_genre_weighted(genre, genre_mapping):
    category_counts = {}
    for broad_category, specific_genres in genre_mapping.items():
        count = sum(1 for specific_genre in specific_genres if specific_genre in genre.lower())
        if count > 0:
            category_counts[broad_category] = count

    if not category_counts:
        return 'others'

    # Find the category with the highest count
    max_count = max(category_counts.values())
    top_categories = [category for category, count in category_counts.items() if count == max_count]

    # Handle ties: select a random category from the top categories
    return random.choice(top_categories)


def map_genres_to_categories(df, genre_mapping):
    df['category'] = df['genre'].apply(lambda genre: map_genre_weighted(genre, genre_mapping))
    return df


def select_scale_train(df):
    features = df[['bpm', 'acousticness', 'danceability', 'energy', 'instrumentalness',
                   'liveness', 'loudness', 'speechiness', 'mode', 'valence']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    neighbors = NearestNeighbors(n_neighbors=1, algorithm='ball_tree')
    neighbors.fit(scaled_features)

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define paths relative to the current directory
    scaler_path = '../static/models/scaler.pkl'
    neighbors_path = '../static/models/neighbors.pkl'

    joblib.dump(scaler, scaler_path)
    joblib.dump(neighbors, neighbors_path)

    return scaled_features, scaler, neighbors


def find_similar_song(neighbors, scaler, df, user_features):
    user_features_scaled = scaler.transform([user_features])
    distances, indices = neighbors.kneighbors(user_features_scaled)
    return df.iloc[indices[0]]


def find_closest_song(user_features):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    # Define paths relative to the current directory
    scaler_path = os.path.join(parent_dir + '/static/models/scaler.pkl')
    neighbors_path = os.path.join(parent_dir + '/static/models/neighbors.pkl')

    scaler = joblib.load(scaler_path)
    neighbors = joblib.load(neighbors_path)
    df = pd.read_csv(os.path.join(parent_dir + '/static/data/songs_data.csv'))

    user_features_scaled = scaler.transform([user_features])
    distances, indices = neighbors.kneighbors(user_features_scaled)

    return df.iloc[indices[0]], df.iloc[indices[0]].to_dict()


def save_markdown_table(df_filtered, file_path):
    md_table = df_filtered.to_markdown(index=True)
    with open(file_path, 'w') as f:
        f.write(md_table)


def apply_pca(scaled_features, n_components=2):
    pca = PCA(n_components=n_components)
    pca_features = pca.fit_transform(scaled_features)
    return pca_features


def plot_pca_clusters(df, pca_features):
    df['PCA1'] = pca_features[:, 0]
    df['PCA2'] = pca_features[:, 1]

    plt.figure(figsize=(28, 12))
    sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='category', palette='tab10', s=100, alpha=0.6)
    plt.title('Genre Clusters using PCA')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend(loc='best', bbox_to_anchor=(1, 1), ncol=1)
    plt.show()


def main():

    file_path = '../static/data/songs_data.csv'
    df = load_data(file_path)

    df = map_genres_to_categories(df, genre_mapping)
    scaled_features, scaler, neighbors = select_scale_train(df)

    user_features = [140, 0.5, 0.8, 0.5, 0.1, 0.2, -7, 0.1, 1, 0.9]  # Example features
    similar_songs, similar_song_dict = find_closest_song(user_features)
    print(similar_song_dict)

    columns_to_display = ['name', 'artists', 'bpm', 'genre', 'key', 'acousticness', 'danceability', 'energy',
                          'instrumentalness', 'liveness', 'loudness', 'speechiness', 'mode', 'valence']
    df_filtered = similar_songs[columns_to_display]

    output_file_path = '../static/data/output.md'
    save_markdown_table(df_filtered, output_file_path)

    # pca_features = apply_pca(scaled_features)
    # plot_pca_clusters(df, pca_features)


if __name__ == "__main__":
    main()
