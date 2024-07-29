<template>
  <div class="mb-4 flex flex-col">
    <label :for="id" class="text-3xl font-bold text-red-600 text-center mb-2">
      {{ question.title }}
    </label>
    <div class="mt-4 grid grid-cols-2 gap-4">
      <div
        v-for="option in question.options"
        :key="option.value"
        class="flex items-center justify-center p-4 border border-gray-300 rounded-md cursor-pointer hover:bg-red-600 text-gray-950 hover:text-white transition-all duration-150 ease-in"
        @click="updateValue(option.value)"
        :class="{
          'bg-red-600 text-white': isSelected(option.value),
        }"
      >
        <input
          :type="type"
          :id="option.value"
          :value="option.value"
          :checked="internalModelValue === option.value"
          @change="updateValue(option.value)"
          class="hidden"
        />
        <label :for="option.value" class="text-lg font-medium cursor-pointer">
          {{ option.label }}
        </label>
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
  selectedOptions: {
    type: Object,
    default: () => ({}),
  },
});

const emit = defineEmits(["update:modelValue"]);
const internalModelValue = ref(props.modelValue);

// Update internalModelValue and emit change
const updateValue = (value) => {
  internalModelValue.value = value;
  emit("update:modelValue", value);
};

// Check if the option is selected
const isSelected = (value) => {
  return internalModelValue.value === value;
};

// Watch for changes in the selected options
watch(
  () => props.selectedOptions[props.id],
  (newValue) => {
    if (newValue !== internalModelValue.value) {
      internalModelValue.value = newValue;
    }
  }
);
</script>
