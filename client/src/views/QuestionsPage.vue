<template>
  <div class="flex flex-col items-center justify-center h-full py-4">
    <h1 class="text-white text-3xl font-bold mb-4">Questions</h1>
    <p class="text-white text-lg text-center mb-4">BPM Value: {{ bpm }}</p>

    <!-- Submission Form -->
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

const fetchBpmFromSession = async () => {
  try {
    const response = await fetch("/api/get-bpm-from-session"); // Adjust URL if needed
    const data = await response.json();
    bpm.value = data.bpm;
  } catch (error) {
    console.error("Error fetching BPM:", error);
  }
};

onMounted(() => {
  fetchBpmFromSession();
});

function getCookie(name) {
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue.pop() : '';
}

const submitQuestions = async () => {
  const csrftoken = getCookie('csrftoken');  // Function to retrieve CSRF token from cookies

  const formData = {
    acousticness: acousticness.value,
    danceability: danceability.value,
    energy: energy.value,
    instrumentalness: instrumentalness.value,
    liveness: liveness.value,
    loudness: loudness.value,
    speechiness: speechiness.value,
    mode: mode.value,
    valence: valence.value,
  };

  try {
    const response = await fetch("/api/submit-questions/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken, // include csrf token
      },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      const result = await response.json();

      console.log("Submitted successfully:", result);
      window.location.href = '/music';
    } else {
      console.error("Failed to submit questions:", response.statusText);
    }
  } catch (error) {
    console.error("Error submitting questions:", error);
  }
};
</script>

<style scoped>
/* Add any scoped styles specific to this page if needed */
</style>
