<template>
  <router-link to="/bpm">
    <button
      class="relative top-0 ml-8 mt-6 w-36 h-8 bg-blue-500 overflow-hidden rounded-lg p-[1px] items-center justify-center hover:bg-blue-300 text-white hover:text-black transition-all duration-150 ease-in font-bold"
    >
      Back
    </button>
  </router-link>
  <div class="flex flex-col items-center justify-center h-full py-4">
    <h1 class="text-white text-4xl font-bold mb-4">Music Preferences</h1>
    <p class="text-white text-2xl text-center mb-4">BPM Value: {{ bpm }}</p>

    <!-- Submission Form -->
    <form @submit.prevent="submitQuestions">
      <QuestionCard
        v-for="(question, key) in QUESTIONS"
        :key="key"
        :question="question"
        v-model="answers[key]"
        :id="key"
        :type="question.type || 'radio'"
        :isRadio="!question.select"
      />

      <p v-if="errorMessage" class="text-red-500 text-2xl mt-2">{{ errorMessage }}</p>

      <button
        type="submit"
        class="inline-flex w-36 h-8 bg-white overflow-hidden rounded-lg p-[1px] mb-4 items-center justify-center mt-4 hover:bg-blue-500 transition-all duration-150 ease-in font-bold mr-96"
      >
        Submit
      </button>
    </form>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import QuestionCard from "../components/QuestionCard.vue";
import { QUESTIONS } from "../constants/index.js";

const bpm = ref(null);
const answers = ref({
  mood: null,
  energyLevel: null,
  instrumentDominance: null,
  ambiance: null,
  complexity: null,
});
const errorMessage = ref('');

const fetchBpmFromSession = async () => {
  try {
    const response = await fetch("/api/get-bpm-from-session");
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
  // Check if all answers are filled
  for (const key in answers.value) {
    if (answers.value[key] === null) {
      errorMessage.value = "Please answer all questions before submitting.";
      return;
    }
  }

  const csrftoken = getCookie('csrftoken');

  const formData = {
    bpm: bpm.value,
    ...answers.value,
  };

  try {
    const response = await fetch("/api/submit-questions/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
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
