<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <h1 class="text-white text-3xl font-bold mb-4">Questions</h1>
    <p class="text-white text-lg text-center">BPM Value: {{ bpm }}</p>
    <form @submit.prevent="submitQuestions">
      <div class="mb-4">
        <label for="acousticness" class="text-white">Acousticness:</label>
        <input type="number" v-model="acousticness" id="acousticness" step="0.01" class="ml-2" />
      </div>
      <div class="mb-4">
        <label for="danceability" class="text-white">Danceability:</label>
        <input type="number" v-model="danceability" id="danceability" step="0.01" class="ml-2"/>
      </div>
      <div class="mb-4">
        <label for="energy" class="text-white">Energy:</label>
        <input type="number" v-model="energy" id="energy" step="0.01" class="ml-2"/>
      </div>
      <div class="mb-4">
        <label for="instrumentalness" class="text-white">Instrumentalness:</label>
        <input type="number" v-model="instrumentalness" id="instrumentalness" step="0.01" class="ml-2"/>
      </div>
      <div class="mb-4">
        <label for="liveness" class="text-white">Liveness:</label>
        <input type="number" v-model="liveness" id="liveness" step="0.01" class="ml-2"/>
      </div>
      <div class="mb-4">
        <label for="loudness" class="text-white">Loudness:</label>
        <input type="number" v-model="loudness" id="loudness" step="0.01" class="ml-2"/>
      </div>
      <div class="mb-4">
        <label for="speechiness" class="text-white">Speechiness:</label>
        <input type="number" v-model="speechiness" id="speechiness" step="0.01" class="ml-2"/>
      </div>
      <div class="mb-4">
        <label for="mode" class="text-white">Mode:</label>
        <input type="number" v-model="mode" id="mode" class="ml-2"/>
      </div>
      <div class="mb-4">
        <label for="valence" class="text-white">Valence:</label>
        <input type="number" v-model="valence" id="valence" step="0.01" class="ml-2"/>
      </div>

      <button type="submit"
        class="inline-flex w-36 h-8 bg-white overflow-hidden rounded-lg p-[1px] mb-4 items-center justify-center mt-4 hover:bg-blue-500 transition-all duration-150 ease-in font-bold"
      >
        Submit
      </button>
    </form>
  </div>
</template>

<script setup>
import {ref, onMounted} from "vue";

const bpm = ref(null);
const acousticness = ref(0.0);
const danceability = ref(0.0);
const energy = ref(0.0);
const instrumentalness = ref(0.0);
const liveness = ref(0.0);
const loudness = ref(0.0);
const speechiness = ref(0.0);
const mode = ref(0);
const valence = ref(0.0);

const fetchBpmFromSession = async () => {
  const response = await fetch("/api/get-bpm-from-session"); // Adjust URL if needed
  const data = await response.json();
  bpm.value = data.bpm;
};

onMounted(() => {
  fetchBpmFromSession();
});

const submitQuestions = async () => {
  const data = {
    acousticness: acousticness.value,
    danceability: danceability.value,
    energy: energy.value,
    instrumentalness: instrumentalness.value,
    liveness: liveness.value,
    loudness: loudness.value,
    speechiness: speechiness.value,
    mode: mode.value,
    valence: valence.value,
    // Add other fields
  };

  const response = await fetch("/api/submit-questions/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();
  if (result.status === "success") {
    alert("Questions submitted successfully");
  } else {
    alert("Error submitting questions");
  }
};
</script>

<style scoped>
/* Add any scoped styles specific to this page if needed */
</style>
