<template>
  <div class="flex flex-col items-center justify-center h-full py-4">
    <h1 class="text-white text-4xl font-bold mb-4">Music Preferences</h1>
    <p class="text-white text-lg text-center mb-4">BPM Value: {{ bpm }}</p>

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

      <button
        type="submit"
        class="inline-flex w-36 h-8 bg-white overflow-hidden rounded-lg p-[1px] mb-4 items-center justify-center mt-4 hover:bg-blue-500 transition-all duration-150 ease-in font-bold"
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
  vocalsPreference: null,
  energyLevel: null,
  instrumentDominance: null,
  ambiance: null,
  tempoPreference: null,
  complexity: null,
});

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
