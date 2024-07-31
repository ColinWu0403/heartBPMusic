import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/",
  build: {
    rollupOptions: {
      output: {
        manualChunks: undefined, // Customize code splitting if needed
      },
    },
  },
  define: {
    "process.env": {},
  },
  plugins: [vue()],
});
