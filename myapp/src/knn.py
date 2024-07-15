import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv('../data/songs_data.csv')

# Select relevant features
features = df[['bpm', 'acousticness', 'danceability', 'energy', 'instrumentalness', 
               'liveness', 'loudness', 'speechiness', 'mode', 'valence']]

# Standardize features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Train Nearest Neighbors model
n_neighbors = 1  # You can adjust this number
neighbors = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree')
neighbors.fit(scaled_features)

# Function to find nearest songs
def find_similar_songs(user_features):
    user_features_scaled = scaler.transform([user_features])
    distances, indices = neighbors.kneighbors(user_features_scaled)
    return df.iloc[indices[0]]

# Example user input
user_features = [120, 0.5, 0.8, 0.5, 0.1, 0.2, -7, 0.1, 1, 0.9]  # Example features

columns_to_display = ['name', 'artists', 'bpm', 'genre', 'key', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'mode', 'valence']
similar_songs = find_similar_songs(user_features)
df_filtered = similar_songs[columns_to_display]

md_table = df_filtered.to_markdown(index=True)

# File path to save the markdown table
file_path = '../data/output.md'

# Write the markdown table to a file
with open(file_path, 'w') as f:
    f.write(md_table)

pca = PCA(n_components=2)
pca_features = pca.fit_transform(scaled_features)

# Add PCA components to the DataFrame
df['PCA1'] = pca_features[:, 0]
df['PCA2'] = pca_features[:, 1]

# Plot the clusters
plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='genre', palette='tab10', s=100, alpha=0.6)
plt.title('Genre Clusters using PCA')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(loc='best', bbox_to_anchor=(1, 1), ncol=1)
plt.show()
