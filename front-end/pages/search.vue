<script setup lang="ts">
import type { Media } from '~/types/media'

useHead({
  title: "Artiverse - Recherche avancée",
  meta: [
    { name: "Page de recherche avancée", content: "Recherche avancée de médias"}
  ]
})

const query = ref('')
const filters = ref({
  mediaType: null as string | null,
  minRating: null as number | null,
  maxRating: null as number | null,
  yearFrom: null as number | null,
  yearTo: null as number | null,
  sortBy: 'relevance'
})

const searchResults = ref<Media[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const totalResults = ref(0)
const currentPage = ref(1)
const resultsPerPage = 12

async function performSearch(searchQuery: string, searchFilters: any) {
  loading.value = true
  error.value = null
  query.value = searchQuery
  filters.value = searchFilters

  try {
    const params = new URLSearchParams()

    if (searchQuery) {
      params.append('q', searchQuery)
    }

    if (searchFilters.mediaType) {
      params.append('media_type', searchFilters.mediaType)
    }

    if (searchFilters.minRating) {
      params.append('min_rating', searchFilters.minRating.toString())
    }

    if (searchFilters.maxRating) {
      params.append('max_rating', searchFilters.maxRating.toString())
    }

    if (searchFilters.yearFrom) {
      params.append('year_from', searchFilters.yearFrom.toString())
    }

    if (searchFilters.yearTo) {
      params.append('year_to', searchFilters.yearTo.toString())
    }

    if (searchFilters.sortBy) {
      params.append('sort_by', searchFilters.sortBy)
    }

    const skip = (currentPage.value - 1) * resultsPerPage
    params.append('skip', skip.toString())
    params.append('limit', resultsPerPage.toString())

    const response = await $fetch<{ items: any[], total: number }>(`/api/v1/media/search?${params.toString()}`)

    // Transform backend response to frontend format
    searchResults.value = response.items.map((item: any) => ({
      id: item.id,
      title: item.title,
      type: item.media_type,
      description: item.synopsis,
      rating: item.average_rating,
      releaseDate: item.release_date,
      image: item.cover_image
    }))

    totalResults.value = response.total

  } catch (e) {
    console.error('Search failed:', e)
    error.value = "La recherche a échoué"
    searchResults.value = []
  } finally {
    loading.value = false
  }
}

function handleSearch(searchQuery: string, searchFilters: any) {
  currentPage.value = 1
  performSearch(searchQuery, searchFilters)
}

function nextPage() {
  const maxPage = Math.ceil(totalResults.value / resultsPerPage)
  if (currentPage.value < maxPage) {
    currentPage.value++
    performSearch(query.value, filters.value)
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    performSearch(query.value, filters.value)
  }
}

function goToPage(page: number) {
  currentPage.value = page
  performSearch(query.value, filters.value)
}

const totalPages = computed(() => Math.ceil(totalResults.value / resultsPerPage))
const hasNextPage = computed(() => currentPage.value < totalPages.value)
const hasPrevPage = computed(() => currentPage.value > 1)

const pageNumbers = computed(() => {
  const pages = []
  const maxPagesToShow = 5

  if (totalPages.value <= maxPagesToShow) {
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i)
    }
  } else {
    // Always show first page
    pages.push(1)

    // Show pages around current page
    let startPage = Math.max(2, currentPage.value - 1)
    let endPage = Math.min(totalPages.value - 1, currentPage.value + 1)

    if (startPage > 2) {
      pages.push('...')
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i)
    }

    if (endPage < totalPages.value - 1) {
      pages.push('...')
    }

    // Always show last page
    pages.push(totalPages.value)
  }

  return pages
})
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-7xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">
    <div class="mb-8">
      <h1 class="text-3xl sm:text-4xl font-display font-bold text-text-primary">
        <span class="gradient-text">Recherche</span> avancée
      </h1>
      <p class="mt-2 text-sm text-text-secondary font-body">
        Trouvez exactement ce que vous cherchez
      </p>
    </div>

    <!-- Search component -->
    <EnhancedSearch @search="handleSearch" />

    <!-- Loading state -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <div class="spinner !h-12 !w-12 !border-4"></div>
      <p class="mt-4 text-text-secondary font-body">Recherche en cours...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="mt-8 glass rounded-xl p-6 border border-red-500/30">
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

    <!-- Results -->
    <div v-else-if="searchResults.length > 0" class="mt-8">
      <!-- Results header -->
      <div class="mb-6 flex items-center justify-between">
        <div>
          <p class="text-sm text-text-secondary font-body">
            <span class="font-semibold text-text-primary">{{ totalResults }}</span>
            résultat{{ totalResults > 1 ? 's' : '' }} trouvé{{ totalResults > 1 ? 's' : '' }}
            <span v-if="query" class="text-text-tertiary">pour "<span class="text-text-primary">"{{ query }}"</span>"</span>
          </p>
        </div>
      </div>

      <!-- Results grid -->
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <MediaShow
          v-for="media in searchResults"
          :key="media.id"
          :media="media"
        />
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="mt-10 flex items-center justify-center gap-2">
        <button
          @click="prevPage"
          :disabled="!hasPrevPage"
          class="px-4 py-2.5 rounded-xl border-2 border-border-color bg-bg-secondary text-text-secondary text-sm font-semibold font-display transition-all duration-200 hover:border-border-color-light hover:bg-bg-tertiary hover:text-text-primary disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:border-border-color disabled:hover:bg-bg-secondary disabled:hover:text-text-secondary"
        >
          ← Précédent
        </button>

        <div class="flex gap-1">
          <button
            v-for="page in pageNumbers"
            :key="page"
            @click="typeof page === 'number' ? goToPage(page) : null"
            :disabled="page === '...'"
            class="w-10 h-10 rounded-xl text-sm font-semibold font-display transition-all duration-200"
            :class="{
              'bg-accent text-white border-2 border-accent': page === currentPage,
              'border-2 border-border-color bg-bg-secondary text-text-secondary hover:border-border-color-light hover:bg-bg-tertiary hover:text-text-primary': page !== currentPage && page !== '...',
              'cursor-default opacity-50': page === '...'
            }"
          >
            {{ page }}
          </button>
        </div>

        <button
          @click="nextPage"
          :disabled="!hasNextPage"
          class="px-4 py-2.5 rounded-xl border-2 border-border-color bg-bg-secondary text-text-secondary text-sm font-semibold font-display transition-all duration-200 hover:border-border-color-light hover:bg-bg-tertiary hover:text-text-primary disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:border-border-color disabled:hover:bg-bg-secondary disabled:hover:text-text-secondary"
        >
          Suivant →
        </button>
      </div>
    </div>

    <!-- No results state -->
    <div v-else-if="!loading && !error" class="mt-8 text-center">
      <div class="mx-auto max-w-md glass rounded-2xl p-10 border border-border-color">
        <div class="mb-4">
          <div class="mx-auto h-20 w-20 rounded-full bg-bg-tertiary/50 flex items-center justify-center">
            <span class="text-4xl">🔍</span>
          </div>
        </div>
        <h3 class="text-xl font-semibold text-text-primary font-display mb-2">
          Aucun résultat trouvé
        </h3>
        <p class="text-sm text-text-secondary font-body">
          Essayez de modifier votre recherche ou vos filtres
        </p>
      </div>
    </div>

    <!-- Navigation link -->
    <div class="mt-12 text-center">
      <NuxtLink
        to="/"
        class="inline-flex items-center text-sm font-semibold text-accent hover:text-accent-hover transition-colors gap-2 group"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform group-hover:-translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Retour à l'accueil
      </NuxtLink>
    </div>
  </div>
</template>