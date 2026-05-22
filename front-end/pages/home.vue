<template>
  <div class="space-y-8">
    <!-- Welcome Section -->
    <div class="text-center py-12">
      <h1 class="text-4xl md:text-5xl font-display font-bold text-text-primary mb-4">
        Bienvenue sur <span class="text-accent">Artiverse</span>
      </h1>
      <p class="text-lg text-text-secondary max-w-2xl mx-auto font-body">
        Explorez et gérez votre collection de médias préférés. Films, séries, jeux, livres — tout au même endroit.
      </p>
    </div>

    <!-- Category Filter -->
    <div class="flex flex-wrap justify-center gap-3">
      <button
        v-for="category in categories"
        :key="category.value"
        type="button"
        class="category-filter-btn"
        :class="[
          { 'category-filter-btn--active': selectedCategory === category.value },
          getCategoryClass(category.value)
        ]"
        @click="selectedCategory = category.value"
      >
        <MediaTypeIcon :type="category.icon" size="small" class="mr-2" />
        {{ category.label }}
      </button>
    </div>

    <!-- Content -->
    <div class="space-y-6">
      <!-- Loading State -->
      <div v-if="pending" class="flex flex-col items-center justify-center py-20">
        <div class="spinner"></div>
        <p class="mt-4 text-text-secondary font-body">Chargement des médias...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="card p-6 border-l-4 border-l-red-500">
        <div class="flex items-start gap-4">
          <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-red-500/20">
            <UIIcon name="warning" size="medium" class="text-red-400" />
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-red-400">Erreur de chargement</h3>
            <p class="mt-2 text-sm text-text-secondary">{{ getErrorMessage(error) }}</p>
            <button
              @click="refresh()"
              class="mt-4 btn-primary text-sm px-4 py-2"
            >
              Réessayer
            </button>
          </div>
        </div>
      </div>

      <!-- Media Grid -->
      <div v-else>
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-2xl font-display font-bold text-text-primary">
            {{ selectedCategoryLabel }}
          </h2>
          <span class="text-text-tertiary font-body">
            {{ filteredMedia.length }} média{{ filteredMedia.length > 1 ? 's' : '' }}
          </span>
        </div>

        <div v-if="filteredMedia.length > 0" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <MediaShow v-for="media in filteredMedia" :key="media.id" :media="media" />
        </div>

        <div v-else class="card p-12 text-center">
          <MediaTypeIcon :type="getEmptyStateIcon()" size="large" class="mb-4 mx-auto" />
          <p class="text-text-secondary italic font-body">
            Aucun média disponible dans cette catégorie pour le moment.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MediaType, type Media } from '~/types/media';
import { useApi } from '~/composables/useApi';
import MediaTypeIcon from '~/components/icons/MediaTypeIcon.vue';
import UIIcon from '~/components/icons/UIIcon.vue';

const { getErrorMessage } = useApi()
const { data: mediaList, pending, error, refresh } = await useFetch<Media[]>('/api/media');

type CategoryValue = 'all' | MediaType

const categories: Array<{ label: string; value: CategoryValue; icon: 'all' | 'movie' | 'series' | 'game' | 'book' }> = [
    { label: 'Tous', value: 'all', icon: 'all' },
    { label: 'Films', value: MediaType.Movie, icon: 'movie' },
    { label: 'Séries', value: MediaType.Serie, icon: 'series' },
    { label: 'Jeux vidéo', value: MediaType.Game, icon: 'game' },
    { label: 'Livres', value: MediaType.Book, icon: 'book' }
]

const selectedCategory = ref<CategoryValue>('all')

const filteredMedia = computed(() => {
  const allMedia = mediaList.value || []
  if (selectedCategory.value === 'all') {
    return allMedia
  }

  return allMedia.filter(media => media.type === selectedCategory.value || media.type === (selectedCategory.value as string))
})

const selectedCategoryLabel = computed(() => {
  return categories.find(category => category.value === selectedCategory.value)?.label || 'Tous'
})

function getCategoryClass(category: CategoryValue): string {
  switch (category) {
    case MediaType.Movie:
      return 'category-filter-btn--movie'
    case MediaType.Serie:
      return 'category-filter-btn--series'
    case MediaType.Game:
      return 'category-filter-btn--game'
    case MediaType.Book:
      return 'category-filter-btn--book'
    default:
      return ''
  }
}

function getEmptyStateIcon(): 'all' | 'movie' | 'series' | 'game' | 'book' {
  switch (selectedCategory.value) {
    case MediaType.Movie:
      return 'movie'
    case MediaType.Serie:
      return 'series'
    case MediaType.Game:
      return 'game'
    case MediaType.Book:
      return 'book'
    default:
      return 'all'
  }
}
</script>