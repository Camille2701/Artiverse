<template>
  <div class="flex h-full flex-col overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm transition-all duration-300 ease-out hover:-translate-y-1 hover:border-accent-light hover:shadow-xl hover:ring-2 hover:ring-accent-light">
    
    <div v-if="props.media.image" class="h-48 w-full overflow-hidden bg-gray-100">
      <img :src="props.media.image" :alt="props.media.title" class="h-full w-full object-cover transition-transform duration-500 hover:scale-110" />
    </div>

    <div class="flex flex-grow flex-col p-7">
      <div class="mb-4 flex items-start justify-between gap-3">
        <h3 class="line-clamp-2 text-xl font-bold text-gray-900" :title="props.media.title">
          {{ props.media.title }}
        </h3>
        <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium" :class="badgeClass(props.media.type)">
          {{ props.media.type }}
        </span>
      </div>

      <div class="mb-4 space-y-1 text-sm text-gray-500">
        <div class="flex items-center">
          <span class="mr-2 font-medium">Note:</span>
          <span class="font-bold text-yellow-500">{{ props.media.rating }}/10</span>
        </div>
        <div class="flex items-center">
          <span class="mr-2 font-medium">Sortie:</span>
          <span>{{ formatDate(props.media.releaseDate) }}</span>
        </div>
      </div>

      <p class="line-clamp-3 flex-grow text-sm text-gray-600" :title="props.media.description">
        {{ props.media.description }}
      </p>
    </div>
  </div>
</template>
<script setup lang="ts">
import { MediaType, type Media } from '~~/types/media';

const props = defineProps<{
  media: Media
}>();

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('fr-FR')
}

function badgeClass(type: MediaType) {
  if (type === MediaType.Movie) {
    return 'bg-purple-100 text-purple-800'
  }

  if (type === MediaType.Game) {
    return 'bg-emerald-100 text-emerald-800'
  }

  if (type === MediaType.Serie) {
    return 'bg-sky-100 text-sky-800'
  }

  if (type === MediaType.Book) {
    return 'bg-amber-100 text-amber-800'
  }

  return 'bg-slate-100 text-slate-800'
}
</script>