<template>
  <div
    class="flex flex-col flex-grow items-center justify-between h-screen relative overflow-hidden"
  >
    <!-- Main Content -->
    <div class="z-10 text-center mt-36 mb-8">
      <h1 class="text-white text-6xl font-bold mb-4">Heart BPM Music</h1>
      <p class="text-white text-lg mb-16">
        Discover music that matches your heart rate.
        <br />
        Enter your BPM to get started!
      </p>
      <button
        class="inline-flex w-72 h-12 bg-red-600 text-lg text-white overflow-hidden rounded-lg p-2 items-center justify-center hover:bg-white hover:text-red-600 transition-all duration-150 ease-in font-bold"
      >
        <router-link
          to="/bpm"
          class="w-full h-full flex items-center justify-center"
          >Get Started
        </router-link>
      </button>
    </div>

    <!-- Heart Signal -->
    <div class="relative w-full mb-80">
      <svg
        class="ecg-signal white-signal"
        viewBox="0 0 1000 110"
        preserveAspectRatio="none"
      >
        <polyline
          fill="none"
          stroke="white"
          stroke-width="2"
          points="0,50 200,50 210,10 220,90 230,50 250,50 300,50 310,5 320,105 330,50 400,50 450,50 460,15 470,85 480,50 500,50 510,10 520,100 530,50 600,50 650,50 660,5 670,95 680,50 750,50 800,50 810,10 820,90 830,50 1000,50"
        />
      </svg>
      <svg
        class="ecg-signal red-signal"
        viewBox="0 0 1000 110"
        preserveAspectRatio="none"
      >
        <polyline
          fill="none"
          stroke="red"
          stroke-width="2"
          points="0,50 200,50 210,10 220,90 230,50 250,50 300,50 310,5 320,105 330,50 400,50 450,50 460,15 470,85 480,50 500,50 510,10 520,100 530,50 600,50 650,50 660,5 670,95 680,50 750,50 800,50 810,10 820,90 830,50 1000,50"
        />
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import anime from "animejs";

const heartPulse = ref(null);

onMounted(() => {
  anime({
    targets: heartPulse.value,
    keyframes: [
      { scale: 1, opacity: 0.8 },
      { scale: 1, opacity: 1 },
    ],
    duration: 1000,
    easing: "easeInOutQuad",
    loop: true,
  });

  anime({
    targets: ".ecg-signal polyline",
    strokeDashoffset: [anime.setDashoffset, 0],
    easing: "easeInOutSine",
    duration: 2000,
    delay: (el, i) => i * 250,
    loop: true,
  });
});
</script>

<style scoped>
.ecg-signal {
  position: absolute;
  width: 100%;
  height: 200px;
}

.white-signal {
  z-index: 2; /* Ensure this is above the red signal */
}

.red-signal {
  z-index: 1; /* Ensure this is below the white signal */
  top: 25px; /* Adjust the offset to your liking */
}
</style>
