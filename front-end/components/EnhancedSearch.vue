<script setup lang="ts">
// @ts-ignore
import type { Media } from '~/types/media'
// @ts-ignore
import { MediaType } from '~/types/media'

const emit = defineEmits<{
  search: [query: string, filters: SearchFilters]
}>()

interface SearchFilters {
  mediaType: string | null
  minRating: number | null
  maxRating: number | null
  yearFrom: number | null
  yearTo: number | null
  sortBy: string
}

const query = ref('')
const mediaType = ref<string | null>(null)
const minRating = ref<number | null>(null)
const maxRating = ref<number | null>(null)
const yearFrom = ref<number | null>(null)
const yearTo = ref<number | null>(null)
const sortBy = ref('relevance')

const mediaTypes = [
  { value: null, label: 'Tous les types' },
  { value: MediaType.Movie, label: 'Films' },
  { value: MediaType.Serie, label: 'Séries' },
  { value: MediaType.Game, label: 'Jeux vidéo' },
  { value: MediaType.Book, label: 'Livres' }
]

const sortOptions = [
  { value: 'relevance', label: 'Pertinence' },
  { value: 'rating', label: 'Note' },
  { value: 'popularity', label: 'Popularité' },
  { value: 'newest', label: 'Plus récent' },
  { value: 'oldest', label: 'Plus ancien' }
]

const showAdvanced = ref(false)

function performSearch() {
  const filters: SearchFilters = {
    mediaType: mediaType.value,
    minRating: minRating.value,
    maxRating: maxRating.value,
    yearFrom: yearFrom.value,
    yearTo: yearTo.value,
    sortBy: sortBy.value
  }

  emit('search', query.value, filters)
}

function resetFilters() {
  mediaType.value = null
  minRating.value = null
  maxRating.value = null
  yearFrom.value = null
  yearTo.value = null
  sortBy.value = 'relevance'
  performSearch()
}

function hasActiveFilters() {
  return mediaType.value !== null ||
         minRating.value !== null ||
         maxRating.value !== null ||
         yearFrom.value !== null ||
         yearTo.value !== null ||
         sortBy.value !== 'relevance'
}

// Watch for changes and auto-search
watch([query, mediaType, minRating, maxRating, yearFrom, yearTo, sortBy], () => {
  performSearch()
})
</script>

<template>
  <div class="space-y-4">
    <!-- Main search bar -->
    <div class="relative">
      <input
        v-model="query"
        type="text"
        placeholder="Rechercher par titre, description..."
        class="input-field pr-10"
        @keyup.enter="performSearch"
      />
      <button
        @click="performSearch"
        class="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-gray-400 hover:text-accent transition-colors"
        aria-label="Rechercher"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </button>
    </div>

    <!-- Advanced filters toggle -->
    <button
      @click="showAdvanced = !showAdvanced"
      class="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-accent transition-colors dark:text-text-secondary"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-4 w-4 transition-transform"
        :class="{ 'rotate-180': showAdvanced }"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
      {{ showAdvanced ? 'Masquer' : 'Afficher' }} les filtres avancés
    </button>

    <!-- Advanced filters -->
    <div
      v-if="showAdvanced"
      class="card p-4 space-y-4 animate-in slide-in-from-top-2 duration-300"
    >
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <!-- Media type filter -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-text-secondary mb-1">
            Type de média
          </label>
          <select
            v-model="mediaType"
            class="input-field"
          >
            <option
              v-for="type in mediaTypes"
              :key="type.value || 'all'"
              :value="type.value"
            >
              {{ type.label }}
            </option>
          </select>
        </div>

        <!-- Rating filters -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-text-secondary mb-1">
            Note minimale
          </label>
          <input
            v-model.number="minRating"
            type="number"
            min="1"
            max="10"
            step="0.5"
            placeholder="1"
            class="input-field"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-text-secondary mb-1">
            Note maximale
          </label>
          <input
            v-model.number="maxRating"
            type="number"
            min="1"
            max="10"
            step="0.5"
            placeholder="10"
            class="input-field"
          />
        </div>

        <!-- Year filters -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-text-secondary mb-1">
            Année minimale
          </label>
          <input
            v-model.number="yearFrom"
            type="number"
            min="1900"
            :max="new Date().getFullYear()"
            placeholder="1900"
            class="input-field"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-text-secondary mb-1">
            Année maximale
          </label>
          <input
            v-model.number="yearTo"
            type="number"
            min="1900"
            :max="new Date().getFullYear() as unknown as number"
            :placeholder="new Date().getFullYear().toString()"
            class="input-field"
          />
        </div>

        <!-- Sort by -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-text-secondary mb-1">
            Trier par
          </label>
          <select
            v-model="sortBy"
            class="input-field"
          >
            <option
              v-for="option in sortOptions"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
        </div>
      </div>

      <!-- Reset button -->
      <div v-if="hasActiveFilters()" class="flex justify-end">
        <button
          @click="resetFilters"
          class="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700 transition-colors dark:text-red-400 dark:hover:text-red-300"
        >
          Réinitialiser les filtres
        </button>
      </div>
    </div>

    <!-- Active filters display -->
    <div v-if="hasActiveFilters() && !showAdvanced" class="flex flex-wrap gap-2">
      <span
        v-if="mediaType"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-accent-movie/10 text-accent-movie dark:bg-accent-movie/20"
      >
        {{ mediaTypes.find(t => t.value === mediaType)?.label }}
      </span>
      <span
        v-if="minRating"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400"
      >
        Note ≥ {{ minRating }}
      </span>
      <span
        v-if="maxRating"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400"
      >
        Note ≤ {{ maxRating }}
      </span>
      <span
        v-if="yearFrom"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400"
      >
        Année ≥ {{ yearFrom }}
      </span>
      <span
        v-if="yearTo"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400"
      >
        Année ≤ {{ yearTo }}
      </span>
      <span
        v-if="sortBy !== 'relevance'"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400"
      >
        {{ sortOptions.find(o => o.value === sortBy)?.label }}
      </span>
      <button
        @click="showAdvanced = true"
        class="text-sm text-accent hover:text-accent-hover transition-colors"
      >
        Modifier
      </button>
    </div>
  </div>
</template>