<template>
  <div class="flex justify-center items-center min-h-[100vh] p-4">
    <SongCard v-if="song" :song="song" />
    <p v-else class="text-white text-2xl">Loading...</p>
  </div>
</template>

<script setup>
import SongCard from "../components/SongCard.vue";
import {onMounted, ref} from "vue";

const song = ref(null);

onMounted(() => {
  getSongData();
  console.log(song.value)
});

const getSongData = async () => {
  try {
    const response = await fetch('/api/get-closest-song/', {
      method: "GET",
      headers: {
      "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      song.value = await response.json();
      console.error('Error fetching song details:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching song details:', error);
  }
}
</script>

<style scoped>
</style>
