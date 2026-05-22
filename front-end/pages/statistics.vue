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
      <h1 class="text-3xl sm:text-4xl font-display font-bold text-text-primary">
        <span class="gradient-text">Mes</span> Statistiques
      </h1>
      <p class="mt-2 text-sm text-text-secondary font-body">
        Découvrez votre activité et vos préférences culturelles
      </p>
    </div>

    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <div class="spinner !h-12 !w-12 !border-4"></div>
      <p class="mt-4 text-text-secondary font-body">Chargement des statistiques...</p>
    </div>

    <div v-else-if="error" class="glass rounded-xl p-6 border border-red-500/30">
      <div class="flex items-start gap-4">
        <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-red-500/20">
          <span class="text-red-400 text-lg">⚠️</span>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-red-400">Erreur</h3>
          <p class="mt-2 text-sm text-red-300">{{ error }}</p>
        </div>
      </div>
    </div>

    <div v-else-if="!isAuthenticated" class="glass rounded-xl p-8 text-center border border-accent/20">
      <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-accent/10 flex items-center justify-center">
        <span class="text-3xl">🔐</span>
      </div>
      <h3 class="text-xl font-semibold text-accent mb-2 font-display">Connexion requise</h3>
      <p class="text-text-secondary font-body mb-6">Connectez-vous pour voir vos statistiques personnelles.</p>
      <NuxtLink
        to="/users/login"
        class="btn-primary px-6 py-3"
      >
        Se connecter
      </NuxtLink>
    </div>

    <div v-else-if="statistics" class="space-y-8">
      <!-- Overview Cards -->
      <div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div class="stat-card text-center">
          <div class="text-4xl font-extrabold text-accent font-display">{{ statistics.total_reviews }}</div>
          <div class="mt-2 text-sm font-medium text-text-secondary font-body">Avis</div>
        </div>
        <div class="stat-card text-center">
          <div class="text-4xl font-extrabold text-accent-game font-display">{{ statistics.total_ratings }}</div>
          <div class="mt-2 text-sm font-medium text-text-secondary font-body">Notes</div>
        </div>
        <div class="stat-card text-center">
          <div class="text-4xl font-extrabold text-accent-series font-display">{{ statistics.total_lists }}</div>
          <div class="mt-2 text-sm font-medium text-text-secondary font-body">Listes</div>
        </div>
        <div class="stat-card text-center">
          <div class="text-4xl font-extrabold text-accent-book font-display">{{ statistics.total_media_in_lists }}</div>
          <div class="mt-2 text-sm font-medium text-text-secondary font-body">Médias listés</div>
        </div>
      </div>

      <!-- Taste Distribution -->
      <div class="card p-6">
        <h3 class="text-xl font-bold text-text-primary mb-6 font-display">
          Répartition des goûts
        </h3>
        <div class="space-y-4">
          <div
            v-for="item in sortedTasteDistribution"
            :key="item.type"
            class="flex items-center gap-4"
          >
            <div class="w-24 text-sm font-medium text-text-secondary font-body">
              {{ getMediaTypeLabel(item.type) }}
            </div>
            <div class="flex-1">
              <div class="h-3 rounded-full bg-bg-tertiary overflow-hidden">
                <div
                  class="h-full rounded-full transition-all duration-500 ease-out"
                  :class="getMediaTypeColor(item.type)"
                  :style="{ width: `${item.percentage}%` }"
                ></div>
              </div>
            </div>
            <div class="w-20 text-right text-sm font-bold text-text-primary font-display">
              {{ item.percentage }}%
            </div>
            <div class="w-16 text-right text-sm text-text-secondary font-body">
              ({{ item.total }})
            </div>
          </div>
        </div>
      </div>

      <!-- Activity by Type -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div class="card p-6">
          <h3 class="text-xl font-bold text-text-primary mb-4 font-display">
            Avis par type
          </h3>
          <div class="space-y-3">
            <div
              v-for="(count, type) in statistics.reviews_by_type"
              :key="`review-${type}`"
              class="flex items-center justify-between"
            >
              <span class="text-sm text-text-secondary font-body">
                {{ getMediaTypeLabel(type) }}
              </span>
              <div class="flex items-center gap-2">
                <div
                  class="h-2 rounded-full"
                  :class="getMediaTypeColor(type)"
                  :style="{ width: `${Math.min(count * 10, 100)}px` }"
                ></div>
                <span class="text-sm font-bold text-text-primary font-display">{{ count }}</span>
              </div>
            </div>
            <div v-if="Object.keys(statistics.reviews_by_type).length === 0" class="text-sm text-text-tertiary font-body italic">
              Aucun avis pour le moment
            </div>
          </div>
        </div>

        <div class="card p-6">
          <h3 class="text-xl font-bold text-text-primary mb-4 font-display">
            Notes par type
          </h3>
          <div class="space-y-3">
            <div
              v-for="(data, type) in statistics.ratings_by_type"
              :key="`rating-${type}`"
              class="space-y-1"
            >
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-text-secondary font-body">
                  {{ getMediaTypeLabel(type) }}
                </span>
                <span class="text-sm font-bold text-text-primary font-display">
                  {{ data.average_score.toFixed(1) }}/10
                </span>
              </div>
              <div class="flex items-center justify-between text-xs text-text-secondary font-body">
                <span>{{ data.count }} note(s)</span>
                <div
                  class="h-1.5 rounded-full bg-bg-tertiary flex-1 mx-2 max-w-[100px]"
                >
                  <div
                    class="h-full rounded-full"
                    :class="getMediaTypeColor(type)"
                    :style="{ width: `${(data.average_score / 10) * 100}%` }"
                  ></div>
                </div>
              </div>
            </div>
            <div v-if="Object.keys(statistics.ratings_by_type).length === 0" class="text-sm text-text-tertiary font-body italic">
              Aucune note pour le moment
            </div>
          </div>
        </div>
      </div>

      <!-- Top Rated Media -->
      <div v-if="statistics.top_rated.length > 0" class="card p-6">
        <h3 class="text-xl font-bold text-text-primary mb-4 font-display">
          Mes coups de cœur (8+/10)
        </h3>
        <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">
          <div
            v-for="item in statistics.top_rated"
            :key="item.media_id"
            class="group"
          >
            <NuxtLink :to="`/media/${item.media_id}`" class="block">
              <div class="relative overflow-hidden rounded-xl bg-bg-tertiary">
                <img
                  v-if="item.cover_image"
                  :src="item.cover_image"
                  :alt="item.title"
                  class="aspect-[2/3] w-full object-cover transition-transform duration-300 group-hover:scale-105"
                />
                <div v-else class="aspect-[2/3] w-full flex items-center justify-center bg-bg-tertiary">
                  <span class="text-2xl">📺</span>
                </div>
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                  <div class="absolute bottom-0 left-0 right-0 p-3">
                    <p class="text-xs font-bold text-white truncate font-display">{{ item.title }}</p>
                    <div class="flex items-center gap-1 mt-1">
                      <span class="text-sm">⭐</span>
                      <span class="text-sm font-bold text-yellow-400 font-display">{{ item.rating }}</span>
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
          class="btn-primary px-6 py-3"
        >
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>
  </div>
</template>