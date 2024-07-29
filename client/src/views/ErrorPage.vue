<!-- src/views/BPM.vue -->
<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <h1 class="text-white text-7xl font-bold mb-4 text-center">
      Error: <span class="text-red-600">404</span>
    </h1>

    <h4 class="text-white text-2xl text-center mb-10">Page Not Found</h4>

    <router-link to="/">
      <button
        class="w-36 h-10 bg-red-600 overflow-hidden rounded-lg p-[1px] items-center justify-center hover:bg-red-400 text-white hover:text-black transition-all duration-150 ease-in font-bold"
      >
        Back To Home
      </button>
    </router-link>
  </div>
</template>

<script setup></script>
