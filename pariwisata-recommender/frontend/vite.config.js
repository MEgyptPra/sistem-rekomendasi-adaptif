import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    watch: {
      // Ignore external/host-driven changes in the whole public/ folder to avoid reload loops
      // We previously ignored only public/assets; expand to entire public to stop favicon/tab reloads.
      ignored: ['**/public/**']
    }
  }
})
