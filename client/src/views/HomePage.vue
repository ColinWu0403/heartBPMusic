<!-- src/views/Home.vue -->
<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <h1 class="text-white text-3xl font-bold mb-4">Home</h1>
    <p class="text-white text-lg text-center">Home Page</p>
    <button
      class="inline-flex w-36 h-8 bg-white overflow-hidden rounded-lg p-[1px] items-center justify-center mt-4 hover:bg-blue-500 transition-all duration-150 ease-in font-bold"
    >
      <router-link to="/bpm">Go to BPM Page</router-link>
    </button>
  </div>
</template>

<script setup></script>

<style scoped>
/* Add any scoped styles specific to this page if needed */
</style>
