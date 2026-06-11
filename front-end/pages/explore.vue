<script setup lang="ts">
import type { Media } from '~/types/media'

useHead({
  title: "Artiverse - Catalogue",
  meta: [{ name: "description", content: "Parcourez et recherchez des médias" }]
})

const route = useRoute()
const router = useRouter()
const { getAllMedia, getTrendingMedia } = useMedia()

// ── URL-driven state ──────────────────────────────────────────────────────────
const searchQuery = computed(() => (route.query.q as string) || '')
const activeType   = computed(() => (route.query.type as string) || '')
const activeSort   = computed(() => (route.query.sort as string) || 'relevance')
const activePage   = computed(() => parseInt((route.query.page as string) || '1'))
const isSearchMode = computed(() => searchQuery.value.trim().length > 0)

// ── Local form state ──────────────────────────────────────────────────────────
const inputQuery = ref('')
const resultsPerPage = 16

// ── Results ───────────────────────────────────────────────────────────────────
const results    = ref<Media[]>([])
const total      = ref(0)
const loading    = ref(false)
const error      = ref<string | null>(null)

const totalPages  = computed(() => Math.ceil(total.value / resultsPerPage))
const pageNumbers = computed(() => {
  const pages: (number | string)[] = []
  if (totalPages.value <= 7) {
    for (let i = 1; i <= totalPages.value; i++) pages.push(i)
  } else {
    pages.push(1)
    const start = Math.max(2, activePage.value - 1)
    const end   = Math.min(totalPages.value - 1, activePage.value + 1)
    if (start > 2) pages.push('...')
    for (let i = start; i <= end; i++) pages.push(i)
    if (end < totalPages.value - 1) pages.push('...')
    pages.push(totalPages.value)
  }
  return pages
})

// ── Catalog ───────────────────────────────────────────────────────────────────
interface CatalogSection { key: string; label: string; emoji: string; mediaType: string | null; items: Media[]; loading: boolean }
const catalogSections = ref<CatalogSection[]>([
  { key: 'trending',   label: 'Tendances',  emoji: '🔥', mediaType: null,        items: [], loading: false },
  { key: 'movie',      label: 'Films',      emoji: '🎬', mediaType: 'movie',      items: [], loading: false },
  { key: 'tv_series',  label: 'Séries',     emoji: '📺', mediaType: 'tv_series',  items: [], loading: false },
  { key: 'video_game', label: 'Jeux vidéo', emoji: '🎮', mediaType: 'video_game', items: [], loading: false },
  { key: 'book',       label: 'Livres',     emoji: '📚', mediaType: 'book',       items: [], loading: false },
])

function mapItem(item: any): Media {
  return {
    id: item.id,
    title: item.title,
    type: item.media_type ?? item.type,
    description: item.synopsis ?? item.description,
    rating: item.average_rating ?? item.rating,
    releaseDate: item.release_date ?? item.releaseDate,
    image: item.cover_image ?? item.image,
  } as Media
}

async function loadCatalog() {
  await Promise.all(catalogSections.value.map(async (section) => {
    section.loading = true
    try {
      if (section.key === 'trending') {
        const res = await getTrendingMedia({ limit: 8 })
        section.items = res.map(mapItem)
      } else {
        const res = await getAllMedia({ limit: 8, media_type: section.mediaType })
        section.items = (res.items || []).map(mapItem)
      }
    } catch { section.items = [] }
    finally  { section.loading = false }
  }))
}

async function performSearch() {
  if (!isSearchMode.value) return
  loading.value = true
  error.value = null
  try {
    const params = new URLSearchParams()
    params.set('q', searchQuery.value)
    if (activeType.value)  params.set('media_type', activeType.value)
    if (activeSort.value)  params.set('sort_by', activeSort.value)
    params.set('skip',  String((activePage.value - 1) * resultsPerPage))
    params.set('limit', String(resultsPerPage))

    const res = await $fetch<{ items: any[]; total: number }>(`/api/v1/media/search?${params}`)
    results.value = res.items.map(mapItem)
    total.value   = res.total
  } catch {
    error.value = 'La recherche a échoué.'
    results.value = []
  } finally {
    loading.value = false
  }
}

// ── Navigation helpers ────────────────────────────────────────────────────────
function pushQuery(patch: Record<string, string | null>) {
  const q: Record<string, string> = {}
  const current = route.query as Record<string, string>
  for (const k of ['q', 'type', 'sort', 'page']) {
    if (k in patch) {
      if (patch[k] !== null && patch[k] !== '') q[k] = patch[k]!
    } else if (current[k]) {
      q[k] = current[k]
    }
  }
  router.push({ path: '/explore', query: q })
}

function submitSearch() {
  const q = inputQuery.value.trim()
  if (!q) return
  pushQuery({ q, page: '1' })
}

function setType(type: string | null) {
  pushQuery({ type: type ?? null, page: '1' })
}

function setSort(sort: string) {
  pushQuery({ sort, page: '1' })
}

function goToPage(page: number | string) {
  if (typeof page !== 'number') return
  pushQuery({ page: String(page) })
}

function clearSearch() {
  router.push('/explore')
}

// ── Reactivity ────────────────────────────────────────────────────────────────
watch(
  () => route.query,
  () => {
    inputQuery.value = searchQuery.value
    if (isSearchMode.value) performSearch()
  },
  { immediate: true, deep: true }
)

onMounted(() => {
  loadCatalog()
})

// ── Filter config ─────────────────────────────────────────────────────────────
const typeFilters = [
  { value: '',           label: 'Tout' },
  { value: 'movie',      label: 'Films' },
  { value: 'tv_series',  label: 'Séries' },
  { value: 'video_game', label: 'Jeux' },
  { value: 'book',       label: 'Livres' },
]

const sortOptions = [
  { value: 'relevance',  label: 'Pertinence' },
  { value: 'rating',     label: 'Meilleures notes' },
  { value: 'popularity', label: 'Popularité' },
  { value: 'newest',     label: 'Plus récents' },
  { value: 'oldest',     label: 'Plus anciens' },
]
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-7xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">

    <!-- ===== SEARCH RESULTS MODE ===== -->
    <template v-if="isSearchMode">

      <!-- Breadcrumb + search bar -->
      <div class="mb-6 space-y-4">
        <div class="flex items-center gap-3">
          <button
            @click="clearSearch"
            class="flex items-center gap-1.5 text-sm text-text-tertiary hover:text-text-primary transition-colors"
          >
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
            Catalogue
          </button>
          <span class="text-text-tertiary">/</span>
          <span class="text-sm text-text-secondary font-body">Résultats</span>
        </div>

        <!-- Search bar -->
        <form @submit.prevent="submitSearch" class="flex gap-2">
          <div class="relative flex-1">
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-tertiary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
            </svg>
            <input
              v-model="inputQuery"
              type="text"
              placeholder="Rechercher un titre..."
              class="w-full rounded-xl border border-border-color bg-bg-secondary pl-10 pr-4 py-3 text-sm text-text-primary placeholder-text-tertiary outline-none focus:border-accent transition-colors"
            />
          </div>
          <button type="submit" class="btn-primary px-6 py-3 text-sm">Rechercher</button>
        </form>

        <!-- Filters -->
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="flex flex-wrap gap-2">
            <button
              v-for="f in typeFilters"
              :key="f.value"
              @click="setType(f.value || null)"
              :class="[
                'px-3 py-1.5 rounded-full text-xs font-semibold transition-all',
                activeType === f.value
                  ? 'bg-accent text-white'
                  : 'bg-bg-secondary text-text-secondary border border-border-color hover:border-accent/50 hover:text-text-primary'
              ]"
            >
              {{ f.label }}
            </button>
          </div>

          <select
            :value="activeSort"
            @change="setSort(($event.target as HTMLSelectElement).value)"
            class="rounded-lg border border-border-color bg-bg-secondary px-3 py-1.5 text-xs text-text-primary outline-none focus:border-accent transition-colors cursor-pointer"
          >
            <option v-for="s in sortOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
          </select>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-24">
        <div class="spinner !h-12 !w-12 !border-4"></div>
        <p class="mt-4 text-text-secondary font-body">Recherche en cours...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="glass rounded-xl p-6 border border-red-500/30">
        <p class="text-red-400 text-sm">{{ error }}</p>
      </div>

      <!-- Results -->
      <template v-else-if="results.length > 0">
        <p class="mb-5 text-sm text-text-secondary font-body">
          <span class="font-semibold text-text-primary">{{ total }}</span>
          résultat{{ total > 1 ? 's' : '' }} pour
          "<span class="text-text-primary">{{ searchQuery }}</span>"
        </p>

        <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          <MediaShow v-for="media in results" :key="media.id" :media="media" />
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="mt-10 flex items-center justify-center gap-2">
          <button
            @click="goToPage(activePage - 1)"
            :disabled="activePage <= 1"
            class="px-4 py-2.5 rounded-xl border border-border-color bg-bg-secondary text-text-secondary text-sm font-semibold transition-all hover:bg-bg-tertiary hover:text-text-primary disabled:opacity-40 disabled:cursor-not-allowed"
          >
            &larr;
          </button>
          <div class="flex gap-1">
            <button
              v-for="page in pageNumbers"
              :key="page"
              @click="goToPage(page)"
              :disabled="page === '...'"
              :class="[
                'w-10 h-10 rounded-xl text-sm font-semibold transition-all',
                page === activePage
                  ? 'bg-accent text-white'
                  : page === '...'
                  ? 'cursor-default text-text-tertiary'
                  : 'border border-border-color bg-bg-secondary text-text-secondary hover:bg-bg-tertiary hover:text-text-primary'
              ]"
            >
              {{ page }}
            </button>
          </div>
          <button
            @click="goToPage(activePage + 1)"
            :disabled="activePage >= totalPages"
            class="px-4 py-2.5 rounded-xl border border-border-color bg-bg-secondary text-text-secondary text-sm font-semibold transition-all hover:bg-bg-tertiary hover:text-text-primary disabled:opacity-40 disabled:cursor-not-allowed"
          >
            &rarr;
          </button>
        </div>
      </template>

      <!-- No results -->
      <div v-else class="flex flex-col items-center justify-center py-24">
        <div class="mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-bg-tertiary/50 text-4xl">🔍</div>
        <h3 class="mb-2 text-xl font-semibold text-text-primary font-display">Aucun résultat</h3>
        <p class="text-sm text-text-secondary font-body">Essayez un autre terme ou retirez des filtres.</p>
      </div>
    </template>

    <!-- ===== CATALOG MODE ===== -->
    <template v-else>
      <div class="mb-8">
        <h1 class="text-3xl font-display font-bold text-text-primary sm:text-4xl">
          <span class="gradient-text">Catalogue</span> de médias
        </h1>
        <p class="mt-2 text-sm text-text-secondary font-body">
          Parcourez films, séries, jeux et livres
        </p>
      </div>

      <div class="space-y-10">
        <div
          v-for="section in catalogSections"
          :key="section.key"
          class="glass rounded-xl p-6 border border-border-color"
        >
          <h2 class="mb-5 flex items-center gap-2 text-2xl font-bold text-text-primary font-display">
            <span>{{ section.emoji }}</span>
            {{ section.label }}
          </h2>

          <div v-if="section.loading" class="flex justify-center py-10">
            <div class="spinner !h-8 !w-8"></div>
          </div>

          <div
            v-else-if="section.items.length > 0"
            class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4"
          >
            <MediaShow v-for="media in section.items" :key="media.id" :media="media" />
          </div>

          <div v-else class="flex flex-col items-center justify-center py-10 text-text-tertiary">
            <span class="text-3xl mb-2">📭</span>
            <p class="text-sm">Aucun contenu disponible</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
