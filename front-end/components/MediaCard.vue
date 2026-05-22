<template>
  <div
    class="card card-hover h-full flex flex-col overflow-hidden group"
    :class="mediaCardClasses"
  >
    <div class="relative">
      <!-- Media type indicator -->
      <div class="absolute top-3 left-3 z-10">
        <span
          class="badge px-3 py-1.5 text-xs font-semibold shadow-lg"
          :class="mediaTypeBadgeClass"
        >
          {{ mediaTypeLabel }}
        </span>
      </div>

      <!-- Media cover image placeholder -->
      <div class="h-52 bg-gradient-to-br from-bg-tertiary to-bg-secondary flex items-center justify-center relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-t from-bg-secondary/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <div v-if="media.coverImage" class="w-full h-full">
          <img
            :src="media.coverImage"
            :alt="media.title"
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
        </div>
        <div v-else class="text-center relative z-10">
          <MediaTypeIcon :type="mediaTypeIcon" size="large" class="mb-2 transition-transform duration-300 group-hover:scale-110 mx-auto" />
          <p class="text-text-tertiary text-sm font-medium">Image non disponible</p>
        </div>
      </div>

      <!-- Rating badge -->
      <div v-if="media.rating" class="absolute top-3 right-3 z-10">
        <div class="glass rounded-lg px-3 py-1.5 flex items-center gap-1.5 shadow-lg backdrop-blur-md">
          <UIIcon name="star" size="small" class="text-yellow-400" />
          <span class="text-text-primary font-bold text-sm">{{ media.rating }}/10</span>
        </div>
      </div>
    </div>

    <div class="p-5 flex flex-col flex-grow relative">
      <!-- Decorative accent line -->
      <div class="absolute top-0 left-5 right-5 h-0.5 bg-gradient-to-r from-transparent via-current to-transparent opacity-0 group-hover:opacity-30 transition-opacity duration-300" :class="mediaCardClasses"></div>

      <!-- Title -->
      <h3 class="font-display font-bold text-xl text-text-primary mb-3 line-clamp-2 group-hover:text-white transition-colors" :title="media.title">
        {{ media.title }}
      </h3>

      <!-- Meta information -->
      <div class="space-y-2 mb-4">
        <div v-if="media.releaseDate" class="flex items-center text-sm">
          <UIIcon name="calendar" size="small" class="text-text-tertiary mr-2" />
          <span class="text-text-secondary font-medium">{{ formatDate(media.releaseDate) }}</span>
        </div>
        <div v-if="media.genre" class="flex items-center text-sm">
          <UIIcon name="tag" size="small" class="text-text-tertiary mr-2" />
          <span class="text-text-secondary font-medium">{{ media.genre }}</span>
        </div>
      </div>

      <!-- Description -->
      <p
        v-if="media.description"
        class="text-text-secondary text-sm mb-4 flex-grow line-clamp-3 font-body leading-relaxed"
        :title="media.description"
      >
        {{ media.description }}
      </p>

      <!-- Actions -->
      <div class="pt-4 border-t border-border-color flex items-center gap-3">
        <slot name="actions" />

        <div class="flex gap-2 ml-auto">
          <button
            @click="$emit('select', media)"
            class="btn-primary text-xs px-4 py-2.5 font-semibold"
          >
            Détails
          </button>
          <button
            @click="$emit('delete', media.id)"
            class="px-3 py-2.5 rounded-xl text-text-tertiary hover:text-red-400 hover:bg-red-400/10 transition-all duration-300 hover:scale-105"
            title="Supprimer"
          >
            <UIIcon name="trash" size="small" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MediaType, type Media } from '~/types/media';
import MediaTypeIcon from '~/components/icons/MediaTypeIcon.vue';
import UIIcon from '~/components/icons/UIIcon.vue';

const props = defineProps<{
  media: Media
}>();

const emit = defineEmits<{
  (e: 'select', media: Media): void;
  (e: 'delete', id: string): void;
}>();

function formatDate(dateStr: string) {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

function getMediaTypeClass(type: MediaType) {
  switch (type) {
    case MediaType.Movie:
      return 'media-movie';
    case MediaType.Serie:
      return 'media-series';
    case MediaType.Game:
      return 'media-game';
    case MediaType.Book:
      return 'media-book';
    default:
      return '';
  }
}

function getMediaTypeBadgeClass(type: MediaType) {
  switch (type) {
    case MediaType.Movie:
      return 'bg-gradient-to-r from-accent-movie to-[#ff5c6b] text-white border border-white/20';
    case MediaType.Serie:
      return 'bg-gradient-to-r from-accent-series to-[#aa5fec] text-white border border-white/20';
    case MediaType.Game:
      return 'bg-gradient-to-r from-accent-game to-[#0ee0e1] text-white border border-white/20';
    case MediaType.Book:
      return 'bg-gradient-to-r from-accent-book to-[#f4d97e] text-white border border-white/20';
    default:
      return 'bg-bg-tertiary text-text-secondary border border-border-color';
  }
}

function getMediaTypeLabel(type: MediaType) {
  switch (type) {
    case MediaType.Movie:
      return 'Film';
    case MediaType.Serie:
      return 'Série';
    case MediaType.Game:
      return 'Jeu';
    case MediaType.Book:
      return 'Livre';
    default:
      return type;
  }
}

function getMediaTypeIcon(type: MediaType) {
  switch (type) {
    case MediaType.Movie:
      return 'movie';
    case MediaType.Serie:
      return 'series';
    case MediaType.Game:
      return 'game';
    case MediaType.Book:
      return 'book';
    default:
      return 'all';
  }
}

const mediaCardClasses = computed(() => {
  return getMediaTypeClass(props.media.type);
});

const mediaTypeBadgeClass = computed(() => {
  return getMediaTypeBadgeClass(props.media.type);
});

const mediaTypeLabel = computed(() => {
  return getMediaTypeLabel(props.media.type);
});

const mediaTypeIcon = computed(() => {
  return getMediaTypeIcon(props.media.type);
});
</script>
