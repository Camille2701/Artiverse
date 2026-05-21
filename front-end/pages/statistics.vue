<script setup lang="ts">
import type { UserStatistics } from '~/types/statistics'
import { MediaType } from '~/types/media'

useHead({
  title: "Artiverse - Mes Statistiques",
  meta: [
    { name: "Page de statistiques utilisateur", content: "Tableau de bord statistiques utilisateur"}
  ]
})

const { user, isAuthenticated } = useAuth()
const { getMyStatistics } = useStatistics()

const statistics = ref<UserStatistics | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  if (isAuthenticated.value) {
    try {
      statistics.value = await getMyStatistics()
    } catch (e) {
      console.error('Failed to fetch statistics:', e)
      error.value = "Impossible de charger les statistiques"
    } finally {
      loading.value = false
    }
  } else {
    loading.value = false
  }
})

function getMediaTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    'movie': 'Films',
    'tv_series': 'Séries',
    'video_game': 'Jeux vidéo',
    'book': 'Livres'
  }
  return labels[type] || type
}

function getMediaTypeColor(type: string): string {
  const colors: Record<string, string> = {
    'movie': 'bg-accent-movie',
    'tv_series': 'bg-accent-series',
    'video_game': 'bg-accent-game',
    'book': 'bg-accent-book'
  }
  return colors[type] || 'bg-slate-500'
}

const sortedTasteDistribution = computed(() => {
  if (!statistics.value) return []

  return Object.entries(statistics.value.taste_distribution)
    .sort((a, b) => b[1].total - a[1].total)
    .map(([type, data]) => ({ type, ...data }))
})

const totalPercentage = computed(() => {
  if (!statistics.value) return 0
  return Object.values(statistics.value.taste_distribution)
    .reduce((sum, item) => sum + item.percentage, 0)
})
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-6xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-extrabold text-gray-900 dark:text-text-primary sm:text-4xl">
        Mes Statistiques
      </h1>
      <p class="mt-2 text-sm text-gray-600 dark:text-text-secondary">
        Découvrez votre activité et vos préférences culturelles
      </p>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="h-12 w-12 animate-spin rounded-full border-b-2 border-accent"></div>
      <p class="ml-3 text-gray-600 dark:text-text-secondary">Chargement des statistiques...</p>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-6 dark:bg-red-900/20 dark:border dark:border-red-800">
      <div class="flex items-start gap-4">
        <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/40">
          <span class="text-red-600 dark:text-red-400">⚠️</span>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-medium text-red-800 dark:text-red-400">Erreur</h3>
          <p class="mt-2 text-sm text-red-700 dark:text-red-300">{{ error }}</p>
        </div>
      </div>
    </div>

    <div v-else-if="!isAuthenticated" class="rounded-md bg-blue-50 p-8 text-center dark:bg-blue-900/20 dark:border dark:border-blue-800">
      <h3 class="text-lg font-medium text-blue-800 dark:text-blue-400 mb-2">Connexion requise</h3>
      <p class="text-blue-700 dark:text-blue-300 mb-4">Connectez-vous pour voir vos statistiques personnelles.</p>
      <NuxtLink
        to="/users/login"
        class="inline-flex items-center rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 dark:focus:ring-offset-bg-secondary"
      >
        Se connecter
      </NuxtLink>
    </div>

    <div v-else-if="statistics" class="space-y-8">
      <!-- Overview Cards -->
      <div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div class="card p-6 text-center">
          <div class="text-3xl font-bold text-accent">{{ statistics.total_reviews }}</div>
          <div class="mt-2 text-sm font-medium text-gray-600 dark:text-text-secondary">Avis</div>
        </div>
        <div class="card p-6 text-center">
          <div class="text-3xl font-bold text-accent-game">{{ statistics.total_ratings }}</div>
          <div class="mt-2 text-sm font-medium text-gray-600 dark:text-text-secondary">Notes</div>
        </div>
        <div class="card p-6 text-center">
          <div class="text-3xl font-bold text-accent-series">{{ statistics.total_lists }}</div>
          <div class="mt-2 text-sm font-medium text-gray-600 dark:text-text-secondary">Listes</div>
        </div>
        <div class="card p-6 text-center">
          <div class="text-3xl font-bold text-accent-book">{{ statistics.total_media_in_lists }}</div>
          <div class="mt-2 text-sm font-medium text-gray-600 dark:text-text-secondary">Médias listés</div>
        </div>
      </div>

      <!-- Taste Distribution -->
      <div class="card p-6">
        <h3 class="text-xl font-bold text-gray-900 dark:text-text-primary mb-6">
          Répartition des goûts
        </h3>
        <div class="space-y-4">
          <div
            v-for="item in sortedTasteDistribution"
            :key="item.type"
            class="flex items-center gap-4"
          >
            <div class="w-24 text-sm font-medium text-gray-700 dark:text-text-secondary">
              {{ getMediaTypeLabel(item.type) }}
            </div>
            <div class="flex-1">
              <div class="h-4 rounded-full bg-gray-200 dark:bg-bg-tertiary overflow-hidden">
                <div
                  class="h-full rounded-full transition-all duration-500 ease-out"
                  :class="getMediaTypeColor(item.type)"
                  :style="{ width: `${item.percentage}%` }"
                ></div>
              </div>
            </div>
            <div class="w-20 text-right text-sm font-bold text-gray-900 dark:text-text-primary">
              {{ item.percentage }}%
            </div>
            <div class="w-16 text-right text-sm text-gray-600 dark:text-text-secondary">
              ({{ item.total }})
            </div>
          </div>
        </div>
      </div>

      <!-- Activity by Type -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div class="card p-6">
          <h3 class="text-xl font-bold text-gray-900 dark:text-text-primary mb-4">
            Avis par type
          </h3>
          <div class="space-y-3">
            <div
              v-for="(count, type) in statistics.reviews_by_type"
              :key="`review-${type}`"
              class="flex items-center justify-between"
            >
              <span class="text-sm text-gray-700 dark:text-text-secondary">
                {{ getMediaTypeLabel(type) }}
              </span>
              <div class="flex items-center gap-2">
                <div
                  class="h-2 rounded-full"
                  :class="getMediaTypeColor(type)"
                  :style="{ width: `${Math.min(count * 10, 100)}px` }"
                ></div>
                <span class="text-sm font-bold text-gray-900 dark:text-text-primary">{{ count }}</span>
              </div>
            </div>
            <div v-if="Object.keys(statistics.reviews_by_type).length === 0" class="text-sm text-gray-500 dark:text-text-secondary italic">
              Aucun avis pour le moment
            </div>
          </div>
        </div>

        <div class="card p-6">
          <h3 class="text-xl font-bold text-gray-900 dark:text-text-primary mb-4">
            Notes par type
          </h3>
          <div class="space-y-3">
            <div
              v-for="(data, type) in statistics.ratings_by_type"
              :key="`rating-${type}`"
              class="space-y-1"
            >
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-gray-700 dark:text-text-secondary">
                  {{ getMediaTypeLabel(type) }}
                </span>
                <span class="text-sm font-bold text-gray-900 dark:text-text-primary">
                  {{ data.average_score.toFixed(1) }}/10
                </span>
              </div>
              <div class="flex items-center justify-between text-xs text-gray-600 dark:text-text-secondary">
                <span>{{ data.count }} note(s)</span>
                <div
                  class="h-1.5 rounded-full bg-gray-200 dark:bg-bg-tertiary flex-1 mx-2 max-w-[100px]"
                >
                  <div
                    class="h-full rounded-full"
                    :class="getMediaTypeColor(type)"
                    :style="{ width: `${(data.average_score / 10) * 100}%` }"
                  ></div>
                </div>
              </div>
            </div>
            <div v-if="Object.keys(statistics.ratings_by_type).length === 0" class="text-sm text-gray-500 dark:text-text-secondary italic">
              Aucune note pour le moment
            </div>
          </div>
        </div>
      </div>

      <!-- Top Rated Media -->
      <div v-if="statistics.top_rated.length > 0" class="card p-6">
        <h3 class="text-xl font-bold text-gray-900 dark:text-text-primary mb-4">
          Mes coups de cœur (8+/10)
        </h3>
        <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">
          <div
            v-for="item in statistics.top_rated"
            :key="item.media_id"
            class="group"
          >
            <NuxtLink :to="`/media/${item.media_id}`" class="block">
              <div class="relative overflow-hidden rounded-lg bg-gray-100 dark:bg-bg-tertiary">
                <img
                  v-if="item.cover_image"
                  :src="item.cover_image"
                  :alt="item.title"
                  class="aspect-[2/3] w-full object-cover transition-transform duration-300 group-hover:scale-105"
                />
                <div v-else class="aspect-[2/3] w-full flex items-center justify-center bg-gray-200 dark:bg-bg-tertiary">
                  <span class="text-2xl">📺</span>
                </div>
                <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                  <div class="absolute bottom-0 left-0 right-0 p-2">
                    <p class="text-xs font-bold text-white truncate">{{ item.title }}</p>
                    <div class="flex items-center gap-1 mt-1">
                      <span class="text-lg">⭐</span>
                      <span class="text-sm font-bold text-yellow-400">{{ item.rating }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-center gap-4">
        <NuxtLink
          to="/"
          class="inline-block rounded-md bg-accent px-5 py-2.5 text-sm font-semibold text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 dark:focus:ring-offset-bg-secondary"
        >
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>
  </div>
</template>