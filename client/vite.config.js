import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/',
  build: {
    // Set appropriate assetsPublicPath based on your deployment setup
    assetsPublicPath: '/',
    // Ensure assets are served with the correct MIME type
    rollupOptions: {
      output: {
        manualChunks: undefined, // or other configuration as needed
      },
    },
  },
  plugins: [vue()],
})
