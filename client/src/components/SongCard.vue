<template>
  <div class="song-detail-card p-8 bg-white rounded shadow-md flex flex-row">
    <div class="min-w-[500px] mr-8">
      <h2 class="text-3xl font-bold">{{ song.name }}</h2>
      <p class="text-lg">{{ song.artists }}</p>
      <p class="text-md"><span class="font-bold">BPM:</span> {{ song.bpm }}</p>
      <p class="text-md"><span class="font-bold">Genres:</span> {{ song.genre }}</p>
      <p class="text-md"><span class="font-bold">Key:</span> {{ getKey(song.key) }}</p>
      <div class="stats mt-4">
        <h3 class="text-2xl font-semibold">Stats:</h3>
        <p class="text-md"><span class="font-bold">Acousticness:</span> {{ song.acousticness }}</p>
        <p class="text-md"><span class="font-bold">Danceability:</span> {{ song.danceability }}</p>
        <p class="text-md"><span class="font-bold">Energy:</span> {{ song.energy }}</p>
        <p class="text-md"><span class="font-bold">Instrumentalness:</span> {{ song.instrumentalness }}</p>
        <p class="text-md"><span class="font-bold">Liveness:</span> {{ song.liveness }}</p>
        <p class="text-md"><span class="font-bold">Loudness:</span> {{ song.loudness }}</p>
        <p class="text-md"><span class="font-bold">Speechiness:</span> {{ song.speechiness }}</p>
        <p class="text-md"><span class="font-bold">Mode:</span> {{ song.mode }}</p>
        <p class="text-md"><span class="font-bold">Valence:</span> {{ song.valence }}</p>
      </div>
    </div>
    <div class="min-w-[460px] flex justify-center items-center w-40 h-90">
      <iframe
        :src="getAlbumCoverUrl(song.uri)"
        width="460"
        height="420"
        allowtransparency="true"
      ></iframe>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  song: {
    type: Object,
    required: true,
  },
});

const keyMapping = [
  'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
];

const getKey = (key) => {
  return keyMapping[key];
};

const getAlbumCoverUrl = (uri) => {
  if (typeof uri === 'string') {
    const spotifyId = uri.split(':').pop();
    return `https://open.spotify.com/embed/track/${spotifyId}`;
  } else {
    console.error('Invalid song URI:', uri);
    return ''; // or handle appropriately for your use case
  }
};
</script>

<style scoped>
.song-detail-card {
  display: flex;
  justify-content: space-between;
}
</style>
