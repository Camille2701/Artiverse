<template>
  <div class="space-y-6">
    <!-- Profile Header -->
    <UserProfileHeader
      :user="user"
      :favorite-media="favoriteMedia"
    />

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="stat-card">
        <div class="flex items-center justify-between">
          <span class="text-2xl">🎬</span>
          <span class="text-text-tertiary text-sm">Films</span>
        </div>
        <p class="text-2xl font-display font-bold text-text-primary mt-2">
          {{ stats.movies }}
        </p>
        <p class="text-text-tertiary text-xs mt-1">visionnés</p>
      </div>

      <div class="stat-card">
        <div class="flex items-center justify-between">
          <span class="text-2xl">📺</span>
          <span class="text-text-tertiary text-sm">Séries</span>
        </div>
        <p class="text-2xl font-display font-bold text-text-primary mt-2">
          {{ stats.series }}
        </p>
        <p class="text-text-tertiary text-xs mt-1">regardées</p>
      </div>

      <div class="stat-card">
        <div class="flex items-center justify-between">
          <span class="text-2xl">🎮</span>
          <span class="text-text-tertiary text-sm">Jeux</span>
        </div>
        <p class="text-2xl font-display font-bold text-text-primary mt-2">
          {{ stats.games }}
        </p>
        <p class="text-text-tertiary text-xs mt-1">joués</p>
      </div>

      <div class="stat-card">
        <div class="flex items-center justify-between">
          <span class="text-2xl">📚</span>
          <span class="text-text-tertiary text-sm">Livres</span>
        </div>
        <p class="text-2xl font-display font-bold text-text-primary mt-2">
          {{ stats.books }}
        </p>
        <p class="text-text-tertiary text-xs mt-1">lus</p>
      </div>
    </div>

    <!-- Charts and Badges -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Radar Chart -->
      <MediaRadarChart :stats="stats" />

      <!-- Badges Display -->
      <div class="glass rounded-xl p-6 border border-white/10">
        <h3 class="text-lg font-display font-semibold text-text-primary mb-4">Badges</h3>
        <div v-if="badges.length === 0" class="text-center py-8">
          <p class="text-text-tertiary italic">Aucun badge débloqué pour le moment</p>
          <p class="text-text-tertiary text-sm mt-2">Continuez à explorer pour en débloquer !</p>
        </div>
        <div v-else class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <Badge
            v-for="badge in badges"
            :key="badge.id"
            :badge="badge"
            size="sm"
            class="cursor-pointer hover:scale-105 transition-transform"
          />
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="glass rounded-xl p-6 border border-white/10">
      <h3 class="text-lg font-display font-semibold text-text-primary mb-4">Activité récente</h3>
      <div v-if="recentActivity.length === 0" class="text-center py-8">
        <p class="text-text-tertiary italic">Aucune activité récente</p>
      </div>
      <div v-else class="space-y-4">
        <div
          v-for="activity in recentActivity"
          :key="activity.id"
          class="flex items-center gap-4 p-3 rounded-lg hover:bg-bg-tertiary/50 transition-colors"
        >
          <div class="text-2xl">{{ activity.icon }}</div>
          <div class="flex-1">
            <p class="text-text-primary font-medium">{{ activity.title }}</p>
            <p class="text-text-secondary text-sm">{{ activity.description }}</p>
          </div>
          <div class="text-text-tertiary text-sm">
            {{ formatDate(activity.date) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import UserProfileHeader from './UserProfileHeader.vue'
import MediaRadarChart from './MediaRadarChart.vue'
import Badge from './Badge.vue'

interface User {
  id: string
  username: string
  email: string
  avatar?: string
  bio?: string
  level?: number
  experiencePoints?: number
}

interface Media {
  id: string
  title: string
  image?: string
  type: string
}

interface Badge {
  id: string
  name: string
  description?: string
  icon?: string
  level?: string
  style: 'flat' | 'gradient' | 'glass' | 'holographic'
  mediaType?: 'movie' | 'series' | 'game' | 'book'
}

interface MediaStats {
  movies: number
  series: number
  games: number
  books: number
}

interface Activity {
  id: string
  icon: string
  title: string
  description: string
  date: string
}

interface Props {
  user: User
  stats: MediaStats
  badges?: Badge[]
  favoriteMedia?: Media[]
  recentActivity?: Activity[]
}

withDefaults(defineProps<Props>(), {
  badges: () => [],
  favoriteMedia: () => [],
  recentActivity: () => []
})

function formatDate(dateStr: string): string {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return "Aujourd'hui"
  if (diffDays === 1) return "Hier"
  if (diffDays < 7) return `Il y a ${diffDays} jours`
  if (diffDays < 30) return `Il y a ${Math.floor(diffDays / 7)} semaines`
  if (diffDays < 365) return `Il y a ${Math.floor(diffDays / 30)} mois`
  return `Il y a ${Math.floor(diffDays / 365)} ans`
}
</script>