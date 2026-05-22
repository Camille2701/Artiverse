<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-display font-bold text-text-primary">
        Via vos connexions
      </h2>
      <p class="text-text-tertiary text-sm font-body">
        Découvrez ce que vos amis recommandent
      </p>
    </div>

    <div v-if="recommendations.length === 0" class="text-center py-12">
      <div class="text-6xl mb-4">🔗</div>
      <p class="text-text-secondary italic font-body">
        Connectez-vous avec d'autres utilisateurs pour voir leurs recommandations
      </p>
      <button class="btn-primary mt-4">
        Trouver des amis
      </button>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="rec in recommendations"
        :key="rec.id"
        class="card p-4 flex gap-4 hover:scale-[1.02] transition-transform"
      >
        <!-- User Avatar -->
        <div class="flex-shrink-0">
          <div class="w-12 h-12 rounded-full bg-bg-tertiary overflow-hidden">
            <img
              v-if="rec.user.avatar"
              :src="rec.user.avatar"
              :alt="rec.user.username"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-2xl">
              👤
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="flex-1 min-w-0">
          <div class="flex items-start justify-between gap-2">
            <div>
              <p class="text-text-primary font-medium font-display">
                {{ rec.user.username }}
              </p>
              <p class="text-text-tertiary text-xs font-body">
                {{ rec.reason }}
              </p>
            </div>
            <span
              class="badge px-2 py-0.5 text-xs"
              :class="getMediaTypeBadgeClass(rec.media.type)"
            >
              {{ getMediaTypeLabel(rec.media.type) }}
            </span>
          </div>

          <h3 class="text-text-primary font-semibold mt-2 font-display">
            {{ rec.media.title }}
          </h3>

          <p v-if="rec.review" class="text-text-secondary text-sm mt-2 line-clamp-2 font-body">
            "{{ rec.review }}"
          </p>

          <div class="flex items-center gap-4 mt-3">
            <div v-if="rec.media.rating" class="flex items-center gap-1">
              <span class="text-yellow-400">★</span>
              <span class="text-text-primary text-sm">{{ rec.media.rating }}/10</span>
            </div>
            <div class="flex items-center gap-3 text-text-tertiary text-sm">
              <button class="hover:text-accent transition-colors flex items-center gap-1">
                <span>❤️</span>
                <span>{{ rec.likes }}</span>
              </button>
              <button class="hover:text-accent transition-colors flex items-center gap-1">
                <span>💬</span>
                <span>{{ rec.comments }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Media Cover -->
        <div class="flex-shrink-0 w-20 h-28 bg-bg-tertiary rounded-lg overflow-hidden">
          <img
            v-if="rec.media.image"
            :src="rec.media.image"
            :alt="rec.media.title"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-2xl">
            {{ getMediaTypeIcon(rec.media.type) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface User {
  id: string
  username: string
  avatar?: string
}

interface Media {
  id: string
  title: string
  type: string
  image?: string
  rating?: number
}

interface Recommendation {
  id: string
  user: User
  media: Media
  reason: string
  review?: string
  likes: number
  comments: number
}

interface Props {
  recommendations: Recommendation[]
}

defineProps<Props>()

function getMediaTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    'movie': 'Film',
    'Movie': 'Film',
    'tv_series': 'Série',
    'Serie': 'Série',
    'video_game': 'Jeu',
    'Game': 'Jeu',
    'book': 'Livre',
    'Book': 'Livre'
  }
  return labels[type] || type
}

function getMediaTypeBadgeClass(type: string) {
  if (type === 'movie' || type === 'Movie') {
    return 'bg-accent-movie/10 text-accent-movie'
  }
  if (type === 'video_game' || type === 'Game') {
    return 'bg-accent-game/10 text-accent-game'
  }
  if (type === 'tv_series' || type === 'Serie') {
    return 'bg-accent-series/10 text-accent-series'
  }
  if (type === 'book' || type === 'Book') {
    return 'bg-accent-book/10 text-accent-book'
  }
  return 'bg-tertiary text-text-secondary'
}

function getMediaTypeIcon(type: string) {
  const icons: Record<string, string> = {
    'movie': '🎬',
    'Movie': '🎬',
    'tv_series': '📺',
    'Serie': '📺',
    'video_game': '🎮',
    'Game': '🎮',
    'book': '📚',
    'Book': '📚'
  }
  return icons[type] || '📄'
}
</script>