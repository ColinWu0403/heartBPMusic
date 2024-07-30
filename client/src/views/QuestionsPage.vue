<template>
  <div class="flex flex-col items-center justify-center h-full py-4">
    <h1 class="text-white text-5xl font-bold mt-8 mb-4">Music Preferences</h1>
    <p class="text-white font-medium text-2xl text-center mb-8">
      BPM Value: {{ bpm }}
    </p>

    <div class="bg-white py-8 px-12 max-w-full rounded">
      <!-- Submission Form -->
      <form v-if="isLastQuestion" @submit.prevent="submitQuestions">
        <QuestionCard
          :question="QUESTIONS[questionKeys[currentQuestion]]"
          v-model="answers[questionKeys[currentQuestion]]"
          :id="questionKeys[currentQuestion]"
          :type="QUESTIONS[questionKeys[currentQuestion]].type || 'radio'"
          :isRadio="!QUESTIONS[questionKeys[currentQuestion]].select"
          :selectedOptions="selectedOptions"
          class="mb-8"
        />

        <div class="flex justify-between items-center mt-4 w-full">
          <router-link v-if="currentQuestion === 0" to="/bpm">
            <button :class="buttonStyles">Back</button>
          </router-link>
          <button v-else @click="prevQuestion" :class="buttonStyles">
            Previous
          </button>

          <div class="flex space-x-2">
            <span
              v-for="(key, index) in questionKeys"
              :key="index"
              :class="{
                'bg-red-600': index === currentQuestion,
                'bg-gray-300': index !== currentQuestion,
              }"
              class="w-3 h-3 rounded-full justify-center align-center mb-4"
            ></span>
          </div>

          <button
            v-if="currentQuestion < questionKeys.length - 1"
            @click="nextQuestion"
            :class="buttonStyles"
          >
            Next
          </button>
          <button
            v-else
            type="submit"
            @click="submitQuestions"
            :class="buttonStyles"
          >
            Submit
          </button>
        </div>

        <p
          v-if="isLastQuestion && errorMessage"
          class="text-red-500 font-medium text-xl mt-2"
        >
          {{ errorMessage }}
        </p>
      </form>

      <div v-else>
        <QuestionCard
          :question="QUESTIONS[questionKeys[currentQuestion]]"
          v-model="answers[questionKeys[currentQuestion]]"
          :id="questionKeys[currentQuestion]"
          :type="QUESTIONS[questionKeys[currentQuestion]].type || 'radio'"
          :isRadio="!QUESTIONS[questionKeys[currentQuestion]].select"
          :selectedOptions="selectedOptions"
          class="mb-8"
        />

        <div class="flex justify-between items-center mt-4 w-full">
          <router-link v-if="currentQuestion === 0" to="/bpm">
            <button :class="buttonStyles">Back</button>
          </router-link>
          <button v-else @click="prevQuestion" :class="buttonStyles">
            Previous
          </button>

          <div class="flex space-x-2">
            <span
              v-for="(key, index) in questionKeys"
              :key="index"
              :class="{
                'bg-red-600': index === currentQuestion,
                'bg-gray-300': index !== currentQuestion,
              }"
              class="w-3 h-3 rounded-full justify-center align-center mb-4"
            ></span>
          </div>

          <button
            v-if="currentQuestion < questionKeys.length - 1"
            @click="nextQuestion"
            :class="buttonStyles"
          >
            Next
          </button>
          <button v-else @click="submitQuestions" :class="buttonStyles">
            Submit
          </button>
        </div>

        <p
          v-if="!isLastQuestion && errorMessage"
          class="text-red-500 font-medium text-xl mt-2"
        >
          {{ errorMessage }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import QuestionCard from "../components/QuestionCard.vue";
import { QUESTIONS } from "../constants/index.js";
import { buttonStyles } from "../constants/styles.js";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const bpm = ref(null);
const currentQuestion = ref(0);
const questionKeys = Object.keys(QUESTIONS);
const answers = ref(
  questionKeys.reduce((acc, key) => ({ ...acc, [key]: null }), {})
);

const selectedOptions = ref({}); // Track selected options for highlighting
const errorMessage = ref("");

// Computed property to get current question key
const currentQuestionKey = computed(() => questionKeys[currentQuestion.value]);

// Check if current question is the last question
const isLastQuestion = computed(
  () => currentQuestion.value === questionKeys.length - 1
);

// Fetch BPM value
const fetchBpmFromSession = async () => {
  const csrftoken = getCookie("csrftoken");

  try {
    const response = await fetch(`${apiBaseUrl}/api/get-bpm-from-session`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
    });
    const data = await response.json();
    bpm.value = data.bpm;
  } catch (error) {
    console.error("Error fetching BPM:", error);
  }
};

onMounted(() => {
  fetchBpmFromSession();
});

// Navigate to the next question
const nextQuestion = () => {
  if (answers.value[currentQuestionKey.value] !== null) {
    if (currentQuestion.value < questionKeys.length - 1) {
      currentQuestion.value++;
      errorMessage.value = "";
    }
  } else {
    errorMessage.value = "Please answer the question before proceeding.";
  }
};

// Navigate to the previous question
const prevQuestion = () => {
  if (currentQuestion.value > 0) {
    currentQuestion.value--;
    errorMessage.value = "";
  }
};

// Update selected options to maintain highlighting
const updateSelectedOptions = () => {
  const key = questionKeys[currentQuestion.value];
  if (answers.value[key] !== null) {
    selectedOptions.value[key] = answers.value[key];
  }
};

// Watch for changes in current question and update selected options
watch(currentQuestion, updateSelectedOptions);

function getCookie(name) {
  const cookieValue = document.cookie.match(
    "(^|;)\\s*" + name + "\\s*=\\s*([^;]+)"
  );
  return cookieValue ? cookieValue.pop() : "";
}

// Handle form submission
const submitQuestions = async () => {
  // Check if all answers are filled
  for (const key of questionKeys) {
    if (answers.value[key] === null) {
      errorMessage.value = "Please answer all questions before submitting.";
      return;
    }
  }
  const csrftoken = getCookie("csrftoken");

  const formData = {
    bpm: bpm.value,
    ...answers.value,
  };

  try {
    const response = await fetch(`${apiBaseUrl}/api/submit-questions/`, {
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
      window.location.href = "/music";
    } else {
      console.error("Failed to submit questions:", response.statusText);
    }
  } catch (error) {
    console.error("Error submitting questions:", error);
  }
};
</script>
