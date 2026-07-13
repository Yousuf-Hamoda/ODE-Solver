import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 8024,
    strictPort: true,
    allowedHosts: ["ode.sofahomelab.xyz", "ode.sofahomelab.io"],
    proxy: {
      '/solve': {
        target: process.env.API_URL || 'http://localhost:5050',
        changeOrigin: true,
      },
    },
  },
})
