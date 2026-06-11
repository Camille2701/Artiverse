// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  runtimeConfig: {
    backendUrl: process.env.BACKEND_URL || 'http://localhost:8000',
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '',
    },
  },
  modules: ['@nuxtjs/tailwindcss', '@nuxtjs/google-fonts'],
  css: ['~/assets/css/main.css'],
  tailwindcss: {
    cssPath: '~/assets/css/main.css',
    configPath: '~/tailwind.config.ts',
  },
  googleFonts: {
    families: {
      SpaceGrotesk: [300, 400, 500, 600, 700],
      Outfit: [300, 400, 500, 600, 700],
      Inter: [300, 400, 500, 600, 700],
    },
    display: 'swap',
    prefetch: true,
    preconnect: true,
  },
  vite: {
    server: {
      watch: {
        usePolling: false,
        interval: 1000
      },
      hmr: true
    },
    optimizeDeps: {
      include: ['vue', '@vue/runtime-core']
    }
  },
})