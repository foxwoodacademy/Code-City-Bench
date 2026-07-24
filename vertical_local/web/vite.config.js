import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Proxy /generate and /presets to backend on port 8000 for local dev
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/generate': 'http://localhost:8000',
      '/presets': 'http://localhost:8000'
    }
  }
})
