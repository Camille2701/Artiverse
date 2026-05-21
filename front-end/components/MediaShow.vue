<template>
  <div class="flex h-full flex-col overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm transition-all duration-300 ease-out hover:-translate-y-1 hover:border-accent-light hover:shadow-xl hover:ring-2 hover:ring-accent-light dark:border-border-color dark:bg-bg-secondary dark:hover:border-accent-movie dark:hover:shadow-xl/50 dark:hover:ring-2 dark:hover:ring-accent-movie/50">

    <NuxtLink :to="`/media/${props.media.id}`" class="block">
      <div v-if="props.media.image" class="h-48 w-full overflow-hidden bg-gray-100 dark:bg-bg-tertiary">
        <img :src="props.media.image" :alt="props.media.title" class="h-full w-full object-cover transition-transform duration-500 hover:scale-110" />
      </div>

      <div class="flex flex-grow flex-col p-7">
        <div class="mb-4 flex items-start justify-between gap-3">
          <h3 class="line-clamp-2 text-xl font-bold text-gray-900 dark:text-text-primary" :title="props.media.title">
            {{ props.media.title }}
          </h3>
          <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium" :class="badgeClass(props.media.type)">
            {{ getMediaTypeLabel(props.media.type) }}
          </span>
        </div>

        <div class="mb-4 space-y-1 text-sm text-gray-500 dark:text-text-secondary">
          <div class="flex items-center">
            <span class="mr-2 font-medium">Note:</span>
            <span class="font-bold text-yellow-500">{{ props.media.rating }}/10</span>
          </div>
          <div class="flex items-center">
            <span class="mr-2 font-medium">Sortie:</span>
            <span>{{ formatDate(props.media.releaseDate) }}</span>
          </div>
        </div>

        <p class="line-clamp-3 flex-grow text-sm text-gray-600 dark:text-text-secondary" :title="props.media.description">
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
  return new Date(dateStr).toLocaleDateString('fr-FR')
}

function getMediaTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    'movie': 'Film',
    'tv_series': 'Série',
    'video_game': 'Jeu vidéo',
    'book': 'Livre'
  }
  return labels[type] || type
}

function badgeClass(type: string) {
  if (type === 'movie' || type === 'Movie') {
    return 'bg-accent-movie/10 text-accent-movie dark:bg-accent-movie/20 dark:text-accent-movie'
  }

  if (type === 'video_game' || type === 'Game') {
    return 'bg-accent-game/10 text-accent-game dark:bg-accent-game/20 dark:text-accent-game'
  }

  if (type === 'tv_series' || type === 'Serie') {
    return 'bg-accent-series/10 text-accent-series dark:bg-accent-series/20 dark:text-accent-series'
  }

  if (type === 'book' || type === 'Book') {
    return 'bg-accent-book/10 text-accent-book dark:bg-accent-book/20 dark:text-accent-book'
  }

  return 'bg-slate-100 text-slate-800 dark:bg-bg-tertiary dark:text-text-secondary'
}
</script>