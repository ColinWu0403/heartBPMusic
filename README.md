# Heart BPM Music

Heart BPMusic is a website that recommends songs based on your heart's BPM (beats per minute) and mood.

The project integrates a Django REST API with a Vue.js frontend to deliver a seamless user experience. It also uses Machine Learning with scikit-learn to provide personalized music recommendations.

### Technologies Used

- **Django REST API:** Serves as the backend for handling requests related to ECG data, BPM calculations, and music recommendations. It processes incoming data, runs the recommendation algorithm, and returns a song recommendation in the form of a spotify url.
- **Vue.js:** Provides an interactive and responsive user interface where users can input their BPM and mood to view song recommendations.
- **scikit-learn:** Powers the recommendation system by analyzing the user input and finds song recommendations. I used scikit-learn's knn model to find the closest matching song to any given parameters.
- **Spotify Web API:** Mainly used to collect song data for my dataset. I created a few python scripts to get a wide variety of artists, where most genres are represented. I then got their top songs' data for my dataset.

### Dataset

I created my own dataset consisting of song characteristics based on how Spotify defines song information in their web API documentation. The dataset of songs includes the song name, artists involved, genres, key, bpm and also includes audio features like mood descriptors and other musical attributes.

#### Spotify Audio Features

The key audio features from Spotify used in the recommendation system include:

- **BPM or Tempo:** Represents the tempo of a song, crucial for matching the user's BPM input with similar songs. This is usually a number between 0 to 200.
- **Genre:** 1 or more genres defined by Spotify to classify the genre of music an artist falls under. Currently, Spotify doesn't list the genre of each specific song, only the genres that describe the corresponding artist.
- **Acousticness:** Reflects the likelihood that a song is acoustic represented by a number from 0.0 to 1.0 where 1.0 means that the track is very likely to be acoustic. This feature is used to match the user's preference for more or less acoustic music.
- **Danceability:** Indicates how suitable a song is for dancing, which helps tailor recommendations based on the user's desired ambiance and complexity. A value of 0.0 is least danceable and 1.0 is most danceable.
- **Energy:** Measures the intensity and activity of a song measure from 0.0 to 1.0 (where 1.0 is the most energetic). This helps in recommending songs that align with the user's mood and energy level preferences. Typically, energetic tracks feel fast, loud, and noisy.
- **Instrumentalness:** Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
- **Key:** Represents the musical key of the track, which affects its harmonic quality and can be important for matching songs with similar tonal characteristics. It is an integer from 0 to 11 representing the key of the song where 0 = C, 1 = C♯/D♭, 2 = D, and so on.
- **Liveness:** Indicates the presence of an audience in the recording, useful for distinguishing between studio and live recordings. A value above 0.8 provides strong likelihood that the track is live.
- **Loudness:** The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. The values typically range between -60 and 0 db (represented as negative floats).
- **Mode:** Refers to the musical mode (major or minor) of the song, affecting the song's emotional quality. It is an integer that is either 1 (major) or 0 (minor).
- **Speechiness:** Measures the presence of spoken words in a track, helping to identify tracks with more speech-like qualities versus more instrumental tracks. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
- **Valence:** Indicates the musical positiveness conveyed by a track, assisting in aligning the mood of the song with the user's mood input. Values closer to 1.0 sound more positive (e.g. happy, cheerful, euphoric), while values closer to 0.0 sound more negative (e.g. sad, depressed, angry).

#### Dataset Stats

The entire dataset of artists can be found in [artists_data.csv](myapp/static/data/artists_data.csv).

The entire dataset of songs can be found in [songs_data.csv](myapp/static/data/songs_data.csv).

I also have two READMEs containing statistics of the artists and songs datasets which can provide some insight on how my dataset looks like: [artists_stats](myapp/static/data/artist_stats.md) and [songs_stats](myapp/static/data/songs_stats.md).

### Setup Project

#### Install Dependencies

```
pip install --no-cache-dir -r requirements.txt
```
