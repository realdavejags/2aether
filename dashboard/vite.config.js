import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'  // ← ADD THIS IMPORT FOR RESOLVE

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')  // ← THIS FIXES PATH RESOLUTION
    }
  },
  build: {
    rollupOptions: {
      input: 'index.html'  // Explicitly set entry to index.html — THIS FIXES THE ERROR
    }
  }
})