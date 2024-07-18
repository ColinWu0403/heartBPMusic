<!-- components/Question.vue -->
<template>
  <div class="mb-4 flex flex-col">
    <label :for="id" class="text-2xl font-bold text-red-500">{{ question.title }}</label>
    <div class="mt-2">
      <div v-for="option in question.options" :key="option.value" class="mb-1 flex items-center space-x-2">
        <input
          :type="type"
          :id="option.value"
          :value="option.value"
          :checked="internalModelValue === option.value"
          @change="updateValue(option.value)"
          class="h-4 w-4"
        />
        <label :for="option.value" class="text-md font-medium text-gray-950">{{ option.label }}</label>
      </div>
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

const updateValue = (value) => {
  internalModelValue.value = value;
};
</script>
