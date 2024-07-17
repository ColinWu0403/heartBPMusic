<!-- components/Question.vue -->
<template>
  <div class="mb-4">
    <label :for="id" class="text-xl font-bold text-white">{{ question.title }}</label>
    <div v-if="isRadio">
      <div v-for="option in question.options" :key="option.value">
        <input :type="type" :id="option.value" :value="option.value" v-model="modelValue" />
        <label :for="option.value" class="text-md text-white">{{ option.label }}</label>
      </div>
    </div>
    <div v-else>cl
      <select v-model="modelValue" :id="id" class="ml-2">
        <option v-for="option in question.options" :key="option.value" :value="option.value" class="text-md text-white">
          {{ option.label }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  question: {
    type: Object,
    required: true,
  },
  modelValue: {
    type: String,
    required: true,
  },
  id: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    default: "radio",
  },
  isRadio: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits(["update:modelValue"]);
const internalModelValue = ref(props.modelValue);

watch(internalModelValue, (newValue) => {
  emit("update:modelValue", newValue);
});
</script>
