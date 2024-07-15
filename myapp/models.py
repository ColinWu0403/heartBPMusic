from django.db import models


# Model for song requests to be stored for the session
class SongRequestFeatures(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    bpm = models.FloatField()
    acousticness = models.FloatField()
    danceability = models.FloatField()
    energy = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    speechiness = models.FloatField()
    mode = models.IntegerField()
    valence = models.FloatField()

    def __str__(self):
        return f"{self.id} - BPM: {self.bpm}"
