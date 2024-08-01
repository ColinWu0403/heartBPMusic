<template>
  <div class="flex flex-col justify-center items-center min-h-[100vh] px-4">
    <h1 class="text-white text-5xl font-bold mb-6">Heart BPM Music</h1>
    <h4 class="text-white text-xl font-medium mb-10 text-center">
      Using our song recommendation algorithm and your heart's bpm,<br />we
      found this to be the closest match:
    </h4>
    <SongCard v-if="song" :song="song" />
    <p v-else class="text-white text-2xl">Loading...</p>
  </div>
</template>

<script setup>
import SongCard from "../components/SongCard.vue";
import { onMounted, ref } from "vue";

const song = ref(null);

onMounted(() => {
  getSongData();
  console.log(song.value);
});

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const getSongData = async () => {
  try {
    const response = await fetch(`${apiBaseUrl}/api/get-closest-song/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include", // Ensure session cookies are sent
    });

    if (response.ok) {
      song.value = await response.json();
      console.error("Error fetching song details:", response.statusText);
    }
  } catch (error) {
    console.error("Error fetching song details:", error);
  }
};
</script>

<style scoped></style>
