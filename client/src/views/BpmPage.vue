<!-- src/views/BPM.vue -->
<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <h1 class="text-white text-3xl font-bold mb-4">BPM</h1>
    <button
      @click="fetchBpm"
      class="inline-flex w-36 h-8 bg-white overflow-hidden rounded-lg p-[1px] mb-4 items-center justify-center mt-4 hover:bg-blue-500 transition-all duration-150 ease-in font-bold"
      :disabled="isLoading"
    >
      <div v-if="isLoading" class="flex items-center">
        <div
          class="w-5 h-5 border-4 border-t-4 border-t-blue-500 border-[#d6d6d6] rounded-full animate-spin"
        ></div>
        <span class="ml-2">Loading...</span>
      </div>
      <span v-else>Fetch BPM</span>
    </button>

    <p class="text-white text-lg text-center">BPM Value: {{ bpm }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";

const bpm = ref(null);
const isLoading = ref(false);

const fetchBpm = async () => {
  try {
    isLoading.value = true;

    const response = await fetch("/api/get-bpm"); // Adjust URL as per your Django server setup
    if (!response.ok) {
      throw new Error("Failed to fetch BPM");
    }
    const data = await response.json();
    bpm.value = data.bpm; // Update bpm.value with the fetched BPM
  } catch (error) {
    console.error("Error fetching BPM:", error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Add any scoped styles specific to this page if needed */
</style>
