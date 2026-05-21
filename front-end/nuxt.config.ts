// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],
  tailwindcss: {
    cssPath: '~/assets/css/main.css',
    configPath: '~/tailwind.config.ts',
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