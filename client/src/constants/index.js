export const QUESTIONS = {
  mood: {
    title: "How would you describe your current mood?",
    options: [
      { label: "Happy", value: "happy" },
      { label: "Sad", value: "sad" },
      { label: "Energetic", value: "energetic" },
      { label: "Calm", value: "calm" },
      { label: "Excited", value: "excited" },
      { label: "Reflective", value: "reflective" },
      { label: "Creative", value: "creative" },
    ],
  },
  energyLevel: {
    title: "How energetic would you like the music to be?",
    options: [
      { label: "Highest energy (powerful, intense)", value: "highest" },
      { label: "High energy (upbeat, cheerful)", value: "high" },
      { label: "Moderate energy (balanced, not too intense)", value: "moderate" },
      { label: "Low energy (calm, relaxed)", value: "low" },
      { label: "Lowest energy (slow, solemn)", value: "lowest" },
    ],
  },
  instrumentDominance: {
    title: "How prominent do you want the instrumental parts to be?",
    options: [
      { label: "Strongly instrumental-focused", value: "instrumental" },
      { label: "Balanced vocals and instruments", value: "balanced" },
      { label: "Strongly vocal-focused", value: "vocals" },
    ],
  },
  ambiance: {
    title: "What kind of ambiance are you looking for in the music?",
    options: [
      { label: "Ambient and atmospheric", value: "ambient" },
      { label: "Clear and direct", value: "clear" },
      { label: "Dynamic and varied", value: "dynamic" },
    ],
  },
  complexity: {
    title: "How complex do you want the musical arrangement to be?",
    options: [
      { label: "Intricate and detailed", value: "intricate" },
      { label: "Simple and straightforward", value: "simple" },
    ],
  },
};
