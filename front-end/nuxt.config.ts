// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  css: ['~/assets/css/main.css'],
  modules: ['@nuxtjs/tailwindcss'],
  srcDir: "app/",

  // Ajoute ce bloc ici :
  devServer: {
    host: '127.0.0.1',
    port: 3000
  }
})