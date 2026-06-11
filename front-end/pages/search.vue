<script setup lang="ts">
import type { Media } from '~/types/media'

useHead({
  title: "Artiverse - Catalogue",
  meta: [{ name: "description", content: "Parcourez et recherchez des médias" }]
})

// @ts-ignore
const { getAllMedia, getTrendingMedia } = useMedia()

// --- Search state ---
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
const hasSearched = ref(false)

// --- Catalog sections state ---
const catalogLoading = ref(false)

interface CatalogSection {
  key: string
  label: string
  emoji: string
  mediaType: string | null
  items: Media[]
  loading: boolean
}

const catalogSections = ref<CatalogSection[]>([
  { key: 'trending', label: 'Top Trending', emoji: '🔥', mediaType: null, items: [], loading: false },
  { key: 'movie', label: 'Films', emoji: '🎬', mediaType: 'movie', items: [], loading: false },
  { key: 'tv_series', label: 'Séries', emoji: '📺', mediaType: 'tv_series', items: [], loading: false },
  { key: 'video_game', label: 'Jeux vidéo', emoji: '🎮', mediaType: 'video_game', items: [], loading: false },
  { key: 'book', label: 'Livres', emoji: '📚', mediaType: 'book', items: [], loading: false },
])

function mapItem(item: any): Media {
  return {
    id: item.id,
    title: item.title,
    type: item.media_type ?? item.type,
    description: item.synopsis ?? item.description,
    rating: item.average_rating ?? item.rating,
    releaseDate: item.release_date ?? item.releaseDate,
    image: item.cover_image ?? item.image
  } as Media
}

async function loadCatalog() {
  catalogLoading.value = true

  await Promise.all(catalogSections.value.map(async (section) => {
    section.loading = true
    try {
      if (section.key === 'trending') {
        const items = await getTrendingMedia({ limit: 8 })
        section.items = items.map(mapItem)
      } else {
        const resp = await getAllMedia({ limit: 8, media_type: section.mediaType })
        section.items = (resp.items || []).map(mapItem)
      }
    } catch {
      section.items = []
    } finally {
      section.loading = false
    }
  }))

  catalogLoading.value = false
}

async function performSearch(searchQuery: string, searchFilters: any) {
  loading.value = true
  error.value = null
  hasSearched.value = true
  query.value = searchQuery
  filters.value = searchFilters

  try {
    const params = new URLSearchParams()
    if (searchQuery) params.append('q', searchQuery)
    if (searchFilters.mediaType) params.append('media_type', searchFilters.mediaType)
    if (searchFilters.minRating) params.append('min_rating', searchFilters.minRating.toString())
    if (searchFilters.maxRating) params.append('max_rating', searchFilters.maxRating.toString())
    if (searchFilters.yearFrom) params.append('year_from', searchFilters.yearFrom.toString())
    if (searchFilters.yearTo) params.append('year_to', searchFilters.yearTo.toString())
    if (searchFilters.sortBy) params.append('sort_by', searchFilters.sortBy)

    const skip = (currentPage.value - 1) * resultsPerPage
    params.append('skip', skip.toString())
    params.append('limit', resultsPerPage.toString())

    const response = await $fetch<{ items: any[], total: number }>(`/api/v1/media/search?${params.toString()}`)
    searchResults.value = response.items.map(mapItem)
    totalResults.value = response.total
  } catch {
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

function clearSearch() {
  hasSearched.value = false
  query.value = ''
  searchResults.value = []
  error.value = null
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
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
  const pages: (number | string)[] = []
  const max = 5

  if (totalPages.value <= max) {
    for (let i = 1; i <= totalPages.value; i++) pages.push(i)
  } else {
    pages.push(1)
    const start = Math.max(2, currentPage.value - 1)
    const end = Math.min(totalPages.value - 1, currentPage.value + 1)
    if (start > 2) pages.push('...')
    for (let i = start; i <= end; i++) pages.push(i)
    if (end < totalPages.value - 1) pages.push('...')
    pages.push(totalPages.value)
  }

  return pages
})

onMounted(() => {
  loadCatalog()
})
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-7xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">
    <!-- Page header -->
    <div class="mb-8">
      <h1 class="text-3xl font-display font-bold text-text-primary sm:text-4xl">
        <span class="gradient-text">Catalogue</span> de médias
      </h1>
      <p class="mt-2 text-sm text-text-secondary font-body">
        Parcourez et recherchez films, séries, jeux et livres
      </p>
    </div>

    <!-- Search component -->
    <EnhancedSearch @search="handleSearch" />

    <!-- "Back to catalogue" link shown when in search mode -->
    <div v-if="hasSearched" class="mt-4">
      <button
        @click="clearSearch"
        class="inline-flex items-center gap-1.5 text-sm font-medium text-accent hover:text-accent-hover transition-colors"
      >
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Retour au catalogue complet
      </button>
    </div>

    <!-- ===== SEARCH MODE ===== -->
    <template v-if="hasSearched">
      <!-- Loading -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-20">
        <div class="spinner !h-12 !w-12 !border-4"></div>
        <p class="mt-4 text-text-secondary font-body">Recherche en cours...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="mt-8 glass rounded-xl p-6 border border-red-500/30">
        <div class="flex items-start gap-4">
          <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-red-500/20">
            <span class="text-red-400 text-lg">⚠️</span>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-red-400">Erreur</h3>
            <p class="mt-1 text-sm text-red-300">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Results -->
      <div v-else-if="searchResults.length > 0" class="mt-8">
        <div class="mb-6 flex items-center justify-between">
          <p class="text-sm text-text-secondary font-body">
            <span class="font-semibold text-text-primary">{{ totalResults }}</span>
            résultat{{ totalResults > 1 ? 's' : '' }} trouvé{{ totalResults > 1 ? 's' : '' }}
            <span v-if="query"> pour "<span class="text-text-primary">{{ query }}</span>"</span>
          </p>
        </div>

        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <MediaShow v-for="media in searchResults" :key="media.id" :media="media" />
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="mt-10 flex items-center justify-center gap-2">
          <button @click="prevPage" :disabled="!hasPrevPage"
            class="px-4 py-2.5 rounded-xl border-2 border-border-color bg-bg-secondary text-text-secondary text-sm font-semibold font-display transition-all hover:border-border-color-light hover:bg-bg-tertiary hover:text-text-primary disabled:opacity-50 disabled:cursor-not-allowed">
            ← Précédent
          </button>
          <div class="flex gap-1">
            <button v-for="page in pageNumbers" :key="page"
              @click="typeof page === 'number' ? goToPage(page) : null"
              :disabled="page === '...'"
              class="w-10 h-10 rounded-xl text-sm font-semibold font-display transition-all"
              :class="{
                'bg-accent text-white border-2 border-accent': page === currentPage,
                'border-2 border-border-color bg-bg-secondary text-text-secondary hover:border-border-color-light hover:bg-bg-tertiary hover:text-text-primary': page !== currentPage && page !== '...',
                'cursor-default opacity-50': page === '...'
              }">
              {{ page }}
            </button>
          </div>
          <button @click="nextPage" :disabled="!hasNextPage"
            class="px-4 py-2.5 rounded-xl border-2 border-border-color bg-bg-secondary text-text-secondary text-sm font-semibold font-display transition-all hover:border-border-color-light hover:bg-bg-tertiary hover:text-text-primary disabled:opacity-50 disabled:cursor-not-allowed">
            Suivant →
          </button>
        </div>
      </div>

      <!-- No results -->
      <div v-else class="mt-8 text-center">
        <div class="mx-auto max-w-md glass rounded-2xl p-10 border border-border-color">
          <div class="mb-4 mx-auto h-20 w-20 rounded-full bg-bg-tertiary/50 flex items-center justify-center">
            <span class="text-4xl">🔍</span>
          </div>
          <h3 class="text-xl font-semibold text-text-primary font-display mb-2">Aucun résultat</h3>
          <p class="text-sm text-text-secondary font-body">Essayez de modifier votre recherche ou vos filtres</p>
        </div>
      </div>
    </template>

    <!-- ===== CATALOG MODE ===== -->
    <template v-else>
      <div class="mt-8 space-y-10">
        <div v-for="section in catalogSections" :key="section.key" class="glass rounded-xl p-6 border border-border-color">
          <h2 class="mb-5 flex items-center gap-2 text-2xl font-bold text-text-primary font-display">
            <span class="text-2xl">{{ section.emoji }}</span>
            {{ section.label }}
          </h2>

          <!-- Section loading -->
          <div v-if="section.loading" class="flex justify-center py-10">
            <div class="spinner !h-8 !w-8 !border-3"></div>
          </div>

          <!-- Section items -->
          <div v-else-if="section.items.length > 0"
            class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-4">
            <MediaShow v-for="media in section.items" :key="media.id" :media="media" />
          </div>

          <!-- Empty section -->
          <div v-else class="flex flex-col items-center justify-center py-10 text-text-tertiary">
            <span class="text-3xl mb-2">📭</span>
            <p class="text-sm">Aucun contenu disponible pour le moment</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
