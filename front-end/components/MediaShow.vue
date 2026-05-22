<template>
  <div
    class="card card-hover h-full flex flex-col overflow-hidden group"
    :class="mediaCardClasses"
  >
    <NuxtLink :to="`/media/${props.media.id}`" class="block h-full">
      <div class="relative">
        <!-- Cover image -->
        <div class="h-56 w-full overflow-hidden bg-gradient-to-br from-bg-tertiary to-bg-secondary">
          <img
            v-if="props.media.image"
            :src="props.media.image"
            :alt="props.media.title"
            class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
          <div v-else class="h-full flex items-center justify-center">
            <span class="text-5xl">{{ mediaTypeIcon }}</span>
          </div>
        </div>

        <!-- Overlays -->
        <div class="absolute inset-0 bg-gradient-to-t from-bg-secondary via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

        <!-- Media type badge -->
        <div class="absolute top-3 left-3 z-10">
          <span
            class="badge px-3 py-1.5 text-xs font-semibold shadow-lg"
            :class="mediaTypeBadgeClass"
          >
            {{ mediaTypeLabel }}
          </span>
        </div>

        <!-- Rating badge -->
        <div v-if="props.media.rating" class="absolute top-3 right-3 z-10">
          <div class="glass rounded-lg px-3 py-1 flex items-center gap-1">
            <span class="text-yellow-400">★</span>
            <span class="text-text-primary font-semibold text-sm">{{ props.media.rating }}/10</span>
          </div>
        </div>

        <!-- Quick actions on hover -->
        <div class="absolute bottom-3 right-3 z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex gap-2">
          <button
            class="glass p-2 rounded-lg hover:bg-white/20 transition-colors"
            title="Ajouter aux favoris"
          >
            ❤️
          </button>
          <button
            class="glass p-2 rounded-lg hover:bg-white/20 transition-colors"
            title="Ajouter à la liste"
          >
            ➕
          </button>
        </div>
      </div>

      <div class="flex flex-grow flex-col p-5">
        <div class="mb-3 flex items-start justify-between gap-3">
          <h3 class="line-clamp-2 font-display font-bold text-lg text-text-primary" :title="props.media.title">
            {{ props.media.title }}
          </h3>
        </div>

        <div class="mb-3 space-y-2 text-sm text-text-secondary">
          <div v-if="props.media.releaseDate" class="flex items-center">
            <span class="mr-2">📅</span>
            <span>{{ formatDate(props.media.releaseDate) }}</span>
          </div>
          <div v-if="props.media.genre" class="flex items-center">
            <span class="mr-2">🏷️</span>
            <span>{{ props.media.genre }}</span>
          </div>
        </div>

        <p class="line-clamp-3 flex-grow text-sm text-text-secondary font-body" :title="props.media.description">
          {{ props.media.description }}
        </p>
      </div>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import { MediaType, type Media } from '~/types/media';

const props = defineProps<{
  media: Media
}>();

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

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
    return 'bg-gradient-to-r from-accent-movie to-[#ff5c6b] text-white border border-white/20'
  }

  if (type === 'video_game' || type === 'Game') {
    return 'bg-gradient-to-r from-accent-game to-[#0ee0e1] text-white border border-white/20'
  }

  if (type === 'tv_series' || type === 'Serie') {
    return 'bg-gradient-to-r from-accent-series to-[#aa5fec] text-white border border-white/20'
  }

  if (type === 'book' || type === 'Book') {
    return 'bg-gradient-to-r from-accent-book to-[#f4d97e] text-white border border-white/20'
  }

  return 'bg-bg-tertiary text-text-secondary border border-border-color'
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

const mediaTypeLabel = computed(() => getMediaTypeLabel(props.media.type))
const mediaTypeBadgeClass = computed(() => getMediaTypeBadgeClass(props.media.type))
const mediaTypeIcon = computed(() => getMediaTypeIcon(props.media.type))
const mediaCardClasses = computed(() => {
  const type = props.media.type
  if (type === 'movie' || type === 'Movie') return 'hover:media-movie-glow'
  if (type === 'tv_series' || type === 'Serie') return 'hover:media-series-glow'
  if (type === 'video_game' || type === 'Game') return 'hover:media-game-glow'
  if (type === 'book' || type === 'Book') return 'hover:media-book-glow'
  return ''
})
</script>