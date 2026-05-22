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
    <div class="relative overflow-hidden bg-gradient-to-br from-bg-primary via-bg-secondary to-bg-primary">
      <!-- Animated background elements -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute -top-40 -right-40 w-96 h-96 bg-accent-movie/20 rounded-full blur-3xl animate-pulse-slow"></div>
        <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-accent-series/20 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 1s;"></div>
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-accent-game/10 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 2s;"></div>
      </div>

      <div class="relative mx-auto max-w-7xl px-4 py-20 sm:px-6 sm:py-28 lg:px-8">
        <div class="text-center">
          <div class="mb-6 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-sm">
            <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            <span class="text-sm text-text-secondary font-medium">Nouvelle version disponible</span>
          </div>
          <h1 class="text-5xl sm:text-6xl lg:text-7xl font-display font-bold text-text-primary mb-6">
            Bienvenue sur <span class="gradient-text">Artiverse</span>
          </h1>
          <p class="mx-auto mt-6 max-w-2xl text-xl text-text-secondary font-body leading-relaxed">
            Votre univers multimédia pour découvrir, noter et partager vos films, séries, jeux vidéo et livres préférés.
          </p>
          <div class="mt-10 flex flex-col sm:flex-row justify-center gap-4">
            <NuxtLink
              to="/users/new"
              class="btn-primary px-8 py-4 text-lg font-semibold flex items-center justify-center gap-2 group"
            >
              Commencer maintenant
              <svg class="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </NuxtLink>
            <NuxtLink
              to="/home"
              class="px-8 py-4 text-lg font-semibold text-text-primary border-2 border-border-color rounded-xl hover:border-border-color-light hover:bg-bg-secondary/50 transition-all duration-300 flex items-center justify-center gap-2"
            >
              <span>🔍</span>
              Explorer le catalogue
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Featured Section -->
    <div v-if="featuredMedia.length > 0" class="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-20 lg:px-8">
      <div class="section-heading">
        <h2>À la une</h2>
      </div>
      <div class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <NuxtLink
          v-for="media in featuredMedia"
          :key="media.id"
          :to="`/media/${media.id}`"
          class="featured-card group overflow-hidden"
        >
          <div class="relative h-56 overflow-hidden bg-bg-tertiary">
            <img
              v-if="media.image"
              :src="media.image"
              :alt="media.title"
              class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-bg-secondary via-transparent to-transparent opacity-60"></div>
            <div class="absolute top-3 right-3 glass rounded-full px-3 py-1.5 text-xs font-semibold text-text-primary backdrop-blur-md">
              {{ getMediaTypeLabel(media.type) }}
            </div>
          </div>
          <div class="p-6 bg-bg-secondary/50 backdrop-blur-sm">
            <h3 class="text-xl font-bold text-text-primary font-display group-hover:text-accent transition-colors">{{ media.title }}</h3>
            <p class="mt-2 text-sm text-text-secondary line-clamp-2 font-body">{{ media.description }}</p>
            <div class="mt-4 flex items-center gap-4">
              <div class="flex items-center gap-1">
                <span class="text-yellow-400">⭐</span>
                <span class="font-semibold text-text-primary">{{ media.rating }}/10</span>
              </div>
              <span v-if="media.releaseDate" class="text-sm text-text-tertiary">
                {{ new Date(media.releaseDate).getFullYear() }}
              </span>
            </div>
          </div>
        </NuxtLink>
      </div>
    </div>

    <!-- Categories Section -->
    <div class="bg-bg-secondary/30">
      <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-20 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl sm:text-4xl font-display font-bold text-text-primary mb-4">Explorer par catégorie</h2>
          <p class="text-text-secondary font-body max-w-2xl mx-auto">Découvrez notre collection organisée par type de média</p>
        </div>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <NuxtLink
            v-for="category in categories"
            :key="category.label"
            :to="`/home?category=${category.type}`"
            class="group relative overflow-hidden rounded-2xl glass p-8 transition-all duration-300 hover:scale-105 hover:shadow-2xl"
          >
            <div class="relative z-10">
              <div class="text-5xl mb-4 transition-transform duration-300 group-hover:scale-110">{{ category.icon }}</div>
              <h3 class="text-2xl font-bold text-text-primary font-display">{{ category.label }}</h3>
              <p class="mt-2 text-sm text-text-secondary font-body">
                {{ getMediaByType(category.type).length }} média{{ getMediaByType(category.type).length > 1 ? 's' : '' }}
              </p>
            </div>
            <div class="absolute inset-0 bg-gradient-to-br from-accent-movie/10 to-accent-series/10 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- Statistics Section -->
    <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-20 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-3xl sm:text-4xl font-display font-bold text-text-primary mb-4">Statistiques</h2>
        <p class="text-text-secondary font-body">En quelques chiffres</p>
      </div>
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div class="stat-card">
          <div class="text-4xl font-extrabold gradient-text font-display">{{ mediaList?.length || 0 }}</div>
          <div class="mt-2 text-sm text-text-secondary font-body">Médias disponibles</div>
        </div>
        <div class="stat-card">
          <div class="text-4xl font-extrabold text-accent-series font-display">4</div>
          <div class="mt-2 text-sm text-text-secondary font-body">Catégories</div>
        </div>
        <div class="stat-card">
          <div class="text-4xl font-extrabold text-accent-game font-display">∞</div>
          <div class="mt-2 text-sm text-text-secondary font-body">Possibilités</div>
        </div>
        <div class="stat-card">
          <div class="text-4xl font-extrabold text-accent-book font-display">100%</div>
          <div class="mt-2 text-sm text-text-secondary font-body">Gratuit</div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="pending" class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div class="flex flex-col items-center justify-center py-20">
        <div class="spinner !h-12 !w-12 !border-4"></div>
        <p class="mt-4 text-text-secondary font-body">Chargement...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div class="glass rounded-xl p-6 border border-red-500/30">
        <div class="flex items-start gap-4">
          <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-red-500/20">
            <span class="text-red-400">⚠️</span>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-red-400">Erreur de chargement</h3>
            <p class="mt-2 text-sm text-red-300">{{ error.message }}</p>
            <button
              @click="refresh()"
              class="mt-4 btn-primary text-sm px-4 py-2"
            >
              Réessayer
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Call to Action -->
    <div class="relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-accent-movie/20 via-accent-series/20 to-accent-game/20"></div>
      <div class="relative mx-auto max-w-7xl px-4 py-20 sm:px-6 sm:py-24 lg:px-8">
        <div class="text-center">
          <h2 class="text-4xl sm:text-5xl font-display font-bold text-text-primary mb-6">Prêt à commencer ?</h2>
          <p class="mx-auto mt-4 max-w-2xl text-xl text-text-secondary font-body">
            Rejoignez la communauté et commencez à explorer votre univers multimédia dès maintenant.
          </p>
          <div class="mt-10 flex flex-col sm:flex-row justify-center gap-4">
            <NuxtLink
              to="/users/new"
              class="btn-primary px-8 py-4 text-lg font-semibold flex items-center justify-center gap-2"
            >
              Créer un compte
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </NuxtLink>
            <NuxtLink
              to="/users/login"
              class="px-8 py-4 text-lg font-semibold text-text-primary border-2 border-border-color rounded-xl hover:border-border-color-light hover:bg-bg-secondary/50 transition-all duration-300"
            >
              Se connecter
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>