<!-- src/views/BPM.vue -->
<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <h1 class="text-white text-3xl font-bold mb-4">BPM</h1>
    <button
      @click="fetchBpm"
      class="inline-flex w-36 h-8 bg-white overflow-hidden rounded-lg p-[1px] mb-4 items-center justify-center mt-4 hover:bg-red-600 hover:text-white transition-all duration-150 ease-in font-bold"
      :disabled="isLoading || hasFetchedBpm"
    >
      <div v-if="isLoading" class="flex items-center">
        <div
          class="w-5 h-5 border-4 border-t-4 border-t-red-600 border-[#d6d6d6] rounded-full animate-spin"
        ></div>
        <span class="ml-2">Loading...</span>
      </div>
      <span v-else>Fetch BPM</span>
    </button>

    <p class="text-white text-lg text-center">BPM Value: {{ bpm }}</p>

    <router-link
      v-if="bpm !== null"
      :to="'/questions'"
      class="inline-flex w-36 h-8 bg-white overflow-hidden rounded-lg p-[1px] mb-4 items-center justify-center mt-4 hover:bg-red-600 transition-all duration-150 ease-in font-bold"
    >
      Next
    </router-link>
  </div>
  <router-link to="/">
    <button
      class="absolute bottom-0 left-0 ml-8 mt-4 mb-6 w-36 h-8 bg-red-600 overflow-hidden rounded-lg p-[1px] items-center justify-center hover:bg-red-400 text-white hover:text-black transition-all duration-150 ease-in font-bold"
    >
      Back
    </button>
  </router-link>
</template>

<script setup>
import { ref } from "vue";

const bpm = ref(null);
const isLoading = ref(false);
const hasFetchedBpm = ref(false);

const fetchBpm = async () => {
  if (hasFetchedBpm.value) return;

  try {
    isLoading.value = true;

    const response = await fetch("/api/get-bpm");
    if (!response.ok) {
      throw new Error("Failed to fetch BPM");
    }
    const data = await response.json();
    bpm.value = data.bpm; // Update bpm.value with the fetched BPM
    hasFetchedBpm.value = true;
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
