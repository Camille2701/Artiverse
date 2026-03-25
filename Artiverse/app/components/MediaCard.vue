<template>
  <div class="flex h-full flex-col overflow-hidden rounded-lg border border-gray-200 bg-white p-7 shadow-sm transition-all duration-300 ease-out hover:-translate-y-1 hover:border-accent-light hover:shadow-xl hover:ring-2 hover:ring-accent-light">
    <div class="flex justify-between items-start mb-4">
      <h3 class="font-bold text-xl text-gray-900 line-clamp-2" :title="media.title">
        {{ media.title }}
      </h3>
      <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium" :class="badgeClass(media.type)">
        {{ media.type }}
      </span>
    </div>
    
    <div class="text-sm text-gray-500 mb-4 space-y-1">
      <div class="flex items-center">
        <span class="font-medium mr-2">Note:</span>
        <span class="text-yellow-500 font-bold">{{ media.rating }}/10</span>
      </div>
      <div class="flex items-center">
        <span class="font-medium mr-2">Sortie:</span>
        <span>{{ formatDate(media.releaseDate) }}</span>
      </div>
    </div>

    <p class="text-gray-600 text-sm mb-6 flex-grow line-clamp-3" :title="media.description">
      {{ media.description }}
    </p>

    <div class="mt-auto pt-4 border-t border-gray-100 flex items-center justify-between gap-4">
      <slot name="actions" />
      
      <div class="flex space-x-2 ml-auto">
        <button 
          @click="$emit('select', media)" 
          class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 transition"
        >
          Détails
        </button>
        <button 
          @click="$emit('delete', media.id)" 
          class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition"
        >
          Supprimer
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MediaType, type Media } from '~~/types/media';

const props = defineProps<{
  media: Media
}>();

const emit = defineEmits<{
  (e: 'select', media: Media): void;
  (e: 'delete', id: string): void;
}>();

function formatDate(dateStr: string) {
    if (!dateStr) return '';
    return new Date(dateStr).toLocaleDateString('fr-FR');
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
