<script setup lang="ts">
import { MediaType } from '~/types/media'

useHead({
  title: "Artiverse - Votre univers multimédia",
  meta: [
    { name: "description", content: "Explorez et gérez votre collection de médias préférés" }
  ]
})

const { data: mediaList, pending, error } = await useFetch<any[]>('/api/media')

const featuredMedia = computed(() => {
  const allMedia = mediaList.value || []
  return allMedia.slice(0, 3)
})

const categories = [
  { label: 'Films', type: MediaType.Movie, icon: '🎬' },
  { label: 'Séries', type: MediaType.Serie, icon: '📺' },
  { label: 'Jeux vidéo', type: MediaType.Game, icon: '🎮' },
  { label: 'Livres', type: MediaType.Book, icon: '📚' }
]

const getMediaTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    'movie': 'Film',
    'tv_series': 'Série',
    'video_game': 'Jeu vidéo',
    'book': 'Livre'
  }
  return labels[type] || type
}

const getMediaByType = (type: MediaType) => {
  const allMedia = mediaList.value || []
  return allMedia.filter(media =>
    media.type === type ||
    (type === MediaType.Movie && media.type === 'movie') ||
    (type === MediaType.Serie && media.type === 'tv_series') ||
    (type === MediaType.Game && media.type === 'video_game') ||
    (type === MediaType.Book && media.type === 'book')
  ).slice(0, 4)
}
</script>

<template>
  <div>
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 text-white">
      <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl font-extrabold sm:text-5xl lg:text-6xl">
            Bienvenue sur Artiverse
          </h1>
          <p class="mx-auto mt-6 max-w-2xl text-xl text-indigo-100">
            Votre univers multimédia pour découvrir, noter et partager vos films, séries, jeux vidéo et livres préférés.
          </p>
          <div class="mt-10 flex justify-center gap-4">
            <NuxtLink
              to="/users/new"
              class="rounded-lg bg-white px-8 py-3 text-base font-medium text-indigo-600 transition-all duration-200 ease-out hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-600 sm:text-lg"
            >
              Commencer maintenant
            </NuxtLink>
            <NuxtLink
              to="/home"
              class="rounded-lg border border-transparent px-8 py-3 text-base font-medium text-white transition-all duration-200 ease-out hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-600 sm:text-lg"
            >
              Explorer le catalogue
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Featured Section -->
    <div v-if="featuredMedia.length > 0" class="mx-auto max-w-7xl px-4 py-12 sm:px-6 sm:py-16 lg:px-8">
      <h2 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">À la une</h2>
      <div class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <NuxtLink
          v-for="media in featuredMedia"
          :key="media.id"
          :to="`/media/${media.id}`"
          class="group overflow-hidden rounded-xl bg-white shadow-lg transition-all duration-300 ease-out hover:shadow-2xl hover:-translate-y-1"
        >
          <div class="relative h-48 overflow-hidden bg-gray-100">
            <img
              v-if="media.image"
              :src="media.image"
              :alt="media.title"
              class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
            />
            <div class="absolute top-2 right-2 rounded-full bg-white/90 px-3 py-1 text-xs font-semibold text-gray-800">
              {{ getMediaTypeLabel(media.type) }}
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-bold text-gray-900">{{ media.title }}</h3>
            <p class="mt-2 text-sm text-gray-600 line-clamp-2">{{ media.description }}</p>
            <div class="mt-4 flex items-center gap-4">
              <div class="flex items-center gap-1">
                <span class="text-yellow-500">⭐</span>
                <span class="font-semibold text-gray-800">{{ media.rating }}/10</span>
              </div>
              <span v-if="media.releaseDate" class="text-sm text-gray-500">
                {{ new Date(media.releaseDate).getFullYear() }}
              </span>
            </div>
          </div>
        </NuxtLink>
      </div>
    </div>

    <!-- Categories Section -->
    <div class="bg-gray-50">
      <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 sm:py-16 lg:px-8">
        <h2 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">Explorer par catégorie</h2>
        <div class="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <NuxtLink
            v-for="category in categories"
            :key="category.label"
            :to="`/home?category=${category.type}`"
            class="group relative overflow-hidden rounded-xl bg-white p-6 shadow-md transition-all duration-300 ease-out hover:shadow-xl hover:-translate-y-1"
          >
            <div class="text-4xl mb-3">{{ category.icon }}</div>
            <h3 class="text-xl font-bold text-gray-900">{{ category.label }}</h3>
            <p class="mt-2 text-sm text-gray-600">
              {{ getMediaByType(category.type).length }} média(s)
            </p>
            <div class="absolute inset-0 -translate-x-full bg-gradient-to-r from-indigo-500/10 to-purple-500/10 transition-transform duration-300 ease-out group-hover:translate-x-0" />
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- Statistics Section -->
    <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 sm:py-16 lg:px-8">
      <h2 class="text-3xl font-extrabold text-gray-900 sm:text-4xl text-center mb-12">Statistiques</h2>
      <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
        <div class="rounded-xl bg-white p-6 text-center shadow-md">
          <div class="text-4xl font-extrabold text-indigo-600">{{ mediaList?.length || 0 }}</div>
          <div class="mt-2 text-sm text-gray-600">Médias disponibles</div>
        </div>
        <div class="rounded-xl bg-white p-6 text-center shadow-md">
          <div class="text-4xl font-extrabold text-purple-600">4</div>
          <div class="mt-2 text-sm text-gray-600">Catégories</div>
        </div>
        <div class="rounded-xl bg-white p-6 text-center shadow-md">
          <div class="text-4xl font-extrabold text-pink-600">∞</div>
          <div class="mt-2 text-sm text-gray-600">Possibilités</div>
        </div>
        <div class="rounded-xl bg-white p-6 text-center shadow-md">
          <div class="text-4xl font-extrabold text-blue-600">100%</div>
          <div class="mt-2 text-sm text-gray-600">Gratuit</div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="pending" class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div class="flex items-center justify-center py-20">
        <div class="h-12 w-12 animate-spin rounded-full border-b-2 border-accent"></div>
        <p class="ml-3 text-gray-600">Chargement...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div class="rounded-md bg-red-50 p-6">
        <div class="flex items-start gap-4">
          <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-red-100">
            <span class="text-red-600">⚠️</span>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-medium text-red-800">Erreur de chargement</h3>
            <p class="mt-2 text-sm text-red-700">{{ error.message }}</p>
            <button
              @click="refresh()"
              class="mt-4 inline-flex items-center rounded-md border border-red-600 bg-transparent px-4 py-2 text-sm font-medium text-red-600 transition-all duration-200 ease-out hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1"
            >
              Réessayer
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Call to Action -->
    <div class="bg-gradient-to-r from-green-500 to-teal-500 text-white">
      <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div class="text-center">
          <h2 class="text-3xl font-extrabold sm:text-4xl">Prêt à commencer ?</h2>
          <p class="mx-auto mt-4 max-w-2xl text-xl text-green-100">
            Rejoignez la communauté et commencez à explorer votre univers multimédia dès maintenant.
          </p>
          <div class="mt-8 flex justify-center gap-4">
            <NuxtLink
              to="/users/new"
              class="rounded-lg bg-white px-8 py-3 text-base font-medium text-green-600 transition-all duration-200 ease-out hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-green-500 sm:text-lg"
            >
              Créer un compte
            </NuxtLink>
            <NuxtLink
              to="/users/login"
              class="rounded-lg border border-transparent px-8 py-3 text-base font-medium text-white transition-all duration-200 ease-out hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-green-500 sm:text-lg"
            >
              Se connecter
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>