<script setup lang="ts">
import type { User } from '~/types/user'
import type { UserStatistics } from '~/types/statistics'
import { MediaType } from '~/types/media'

useHead({
  title: "Artiverse - Profil",
  meta: [
    { name: "Page de consultation d'un utilisateur", content: "Consultation d'un utilisateur"}
  ]
})

const { user: currentUser, isAuthenticated, logout } = useAuth()
const { getMyStatistics } = useStatistics()
const { getUserRatings } = useRatings()

const user = ref<User | null>(null)
const error = ref(false)
const loading = ref(true)

const statistics = ref<UserStatistics | null>(null)
const currentView = ref<'collection' | 'statistics'>('collection')
const selectedMediaType = ref<string | null>(null)

// Collection : médias notés par l'utilisateur, groupés par type
interface RatedMedia { media: any; score: number }
const collectionByType = ref<Record<string, RatedMedia[]>>({
  movie: [], tv_series: [], video_game: [], book: []
})
const collectionLoading = ref(false)

const collectionSections = [
  { key: 'movie',      label: 'Films',      emoji: '🎬' },
  { key: 'tv_series',  label: 'Séries',     emoji: '📺' },
  { key: 'video_game', label: 'Jeux vidéo', emoji: '🎮' },
  { key: 'book',       label: 'Livres',     emoji: '📚' },
]

const visibleSections = computed(() =>
  selectedMediaType.value
    ? collectionSections.filter(s => s.key === selectedMediaType.value)
    : collectionSections
)

const mediaTypeFilters = [
  { value: null,              label: 'Tout' },
  { value: MediaType.Movie,   label: 'Films' },
  { value: MediaType.Serie,   label: 'Séries' },
  { value: MediaType.Game,    label: 'Jeux vidéo' },
  { value: MediaType.Book,    label: 'Livres' },
]

const totalRated = computed(() =>
  Object.values(collectionByType.value).reduce((sum, arr) => sum + arr.length, 0)
)

function normalizeMedia(raw: any): any {
  return {
    id: raw.id,
    title: raw.title,
    type: raw.media_type?.value ?? raw.media_type ?? raw.type,
    description: raw.synopsis ?? raw.description,
    rating: raw.average_rating ?? raw.rating,
    releaseDate: raw.release_date ?? raw.releaseDate,
    image: raw.cover_image ?? raw.image,
  }
}

async function loadCollection() {
  if (!isAuthenticated.value || !currentUser.value) return
  collectionLoading.value = true
  try {
    const resp = await getUserRatings({ limit: 200 })
    if (!resp?.items?.length) return

    const ratings = resp.items
    const mediaResults = await Promise.all(
      ratings.map(r => $fetch<any>(`/api/v1/media/${r.media_id}`).catch(() => null))
    )

    const fresh: Record<string, RatedMedia[]> = { movie: [], tv_series: [], video_game: [], book: [] }
    mediaResults.forEach((raw, i) => {
      if (!raw) return
      const media = normalizeMedia(raw)
      const type: string = media.type
      if (fresh[type]) {
        fresh[type].push({ media, score: ratings[i].score })
      }
    })

    // Trier par note de l'utilisateur (décroissant)
    for (const type of Object.keys(fresh)) {
      fresh[type].sort((a, b) => b.score - a.score)
    }

    collectionByType.value = fresh
  } catch (e: any) {
    console.error('Failed to load collection:', e?.statusMessage ?? e?.message ?? e)
  } finally {
    collectionLoading.value = false
  }
}

onMounted(async () => {
  try {
    if (isAuthenticated.value && currentUser.value) {
      user.value = currentUser.value
      try {
        statistics.value = await getMyStatistics()
      } catch {}
      await loadCollection()
    }
  } catch (e) {
    console.error('Failed to fetch user data:', e)
    error.value = true
  } finally {
    loading.value = false
  }
})

function getMediaTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    'movie': 'Films', 'tv_series': 'Séries', 'video_game': 'Jeux vidéo', 'book': 'Livres'
  }
  return labels[type] || type
}

function getMediaTypeHex(type: string): string {
  const hexes: Record<string, string> = {
    'movie': '#FF4757', 'tv_series': '#9B51E0', 'video_game': '#00D2D3', 'book': '#ECCC68'
  }
  return hexes[type] || '#6366f1'
}

async function handleLogout() {
  logout()
  await navigateTo('/')
}
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-6xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">
    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <div class="spinner !h-12 !w-12 !border-4"></div>
      <p class="mt-4 text-text-secondary font-body">Chargement...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="glass rounded-xl p-8 text-center border border-red-500/30">
      <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-red-500/20 flex items-center justify-center">
        <span class="text-3xl">⚠️</span>
      </div>
      <h2 class="mb-4 text-xl font-semibold text-red-400 font-display">Erreur de chargement</h2>
      <NuxtLink
        to="/"
        class="btn-primary px-6 py-3"
      >
        Retour à l'accueil
      </NuxtLink>
    </div>

    <!-- Not Authenticated -->
    <div v-else-if="!isAuthenticated || !user" class="glass rounded-xl p-8 text-center border border-accent/20">
      <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-accent/10 flex items-center justify-center">
        <span class="text-3xl">🔐</span>
      </div>
      <p class="mb-4 text-text-secondary font-body">Vous devez être connecté pour voir votre profil.</p>
      <NuxtLink
        to="/users/login"
        class="btn-primary px-6 py-3"
      >
        Se connecter
      </NuxtLink>
    </div>

    <!-- Profile Content -->
    <div v-else class="space-y-8">
      <!-- Profile Header -->
      <div class="glass rounded-2xl p-6 sm:p-8 border border-white/10">
        <div class="flex flex-col items-center gap-6 text-center sm:flex-row sm:items-center sm:gap-8 sm:text-left">
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-br from-accent-movie via-accent-series to-accent-game rounded-full blur-sm opacity-60"></div>
            <img
              :src="user.avatar_url || 'https://i.pravatar.cc/150?img=12'"
              :alt="user.username"
              class="relative h-28 w-28 sm:h-[120px] sm:w-[120px] lg:h-[130px] lg:w-[130px] rounded-full object-cover border-4 border-bg-secondary"
            />
          </div>
          <div class="flex-1">
            <h1 class="mb-2 text-3xl font-bold text-text-primary font-display sm:text-4xl">{{ user.username }}</h1>
            <p v-if="user.bio" class="mb-4 text-text-secondary font-body">{{ user.bio }}</p>
            <!-- XP progress bar -->
            <div class="w-full max-w-sm">
              <div class="flex justify-between text-xs text-text-tertiary mb-1.5">
                <span class="font-semibold text-text-secondary">Niv. {{ user.level }}</span>
                <span>{{ user.experience_points }} / {{ 100 * user.level ** 2 }} XP</span>
                <span class="font-semibold text-text-secondary">Niv. {{ user.level + 1 }}</span>
              </div>
              <div class="h-2.5 w-full rounded-full overflow-hidden" style="background: rgba(255,255,255,0.08)">
                <div
                  class="h-full rounded-full transition-all duration-500"
                  style="background: linear-gradient(90deg, #3b82f6, #a855f7)"
                  :style="{
                    width: Math.min(100, Math.max(2,
                      ((user.experience_points - 100 * (user.level - 1) ** 2) /
                       (100 * user.level ** 2 - 100 * (user.level - 1) ** 2)) * 100
                    )) + '%'
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistics Section -->
      <div v-if="statistics" class="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div class="stat-card text-center">
          <div class="text-3xl sm:text-4xl font-extrabold text-accent font-display">{{ statistics.total_reviews }}</div>
          <div class="mt-2 text-sm font-medium text-text-secondary font-body">Avis</div>
        </div>
        <div class="stat-card text-center">
          <div class="text-3xl sm:text-4xl font-extrabold text-accent-game font-display">{{ statistics.total_ratings }}</div>
          <div class="mt-2 text-sm font-medium text-text-secondary font-body">Notes</div>
        </div>
        <div class="stat-card text-center">
          <div class="text-3xl sm:text-4xl font-extrabold text-accent-series font-display">{{ statistics.total_lists }}</div>
          <div class="mt-2 text-sm font-medium text-text-secondary font-body">Listes</div>
        </div>
        <div class="stat-card text-center">
          <div class="text-3xl sm:text-4xl font-extrabold text-accent-book font-display">{{ statistics.total_media_in_lists }}</div>
          <div class="mt-2 text-sm font-medium text-text-secondary font-body">Médias listés</div>
        </div>
      </div>

      <!-- View Toggle -->
      <div class="glass rounded-xl p-4 border border-border-color">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <h2 class="text-lg font-semibold text-text-primary font-display">Affichage</h2>
            <p class="text-sm text-text-secondary font-body">Choisissez ce que vous voulez voir</p>
          </div>
          <div class="flex items-center gap-2 bg-bg-tertiary/50 rounded-lg p-1">
            <button
              @click="currentView = 'collection'"
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-all duration-200',
                currentView === 'collection'
                  ? 'bg-accent text-white shadow-lg'
                  : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
              ]"
            >
              Ma Collection
            </button>
            <button
              @click="currentView = 'statistics'"
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-all duration-200',
                currentView === 'statistics'
                  ? 'bg-accent text-white shadow-lg'
                  : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
              ]"
            >
              Statistiques
            </button>
          </div>
        </div>
      </div>

      <!-- Statistics Detail View -->
      <div v-if="currentView === 'statistics' && statistics" class="space-y-6">
        <!-- Taste Distribution -->
        <div class="glass rounded-xl p-6 border border-border-color">
          <h3 class="text-xl font-bold text-text-primary mb-4 font-display">
            Répartition des goûts
          </h3>
          <div class="space-y-4">
            <div
              v-for="(item, type) in statistics.taste_distribution"
              :key="type"
              class="flex items-center gap-4"
            >
              <div class="w-24 text-sm font-medium text-text-secondary font-body">
                {{ getMediaTypeLabel(type) }}
              </div>
              <div class="flex-1">
                <div class="h-3 rounded-full bg-bg-tertiary overflow-hidden">
                  <div
                    class="h-full rounded-full transition-all duration-500 ease-out"
                    :style="{ width: `${item.percentage}%`, backgroundColor: getMediaTypeHex(type) }"
                  ></div>
                </div>
              </div>
              <div class="w-20 text-right text-sm font-bold text-text-primary font-display">
                {{ item.percentage }}%
              </div>
              <div class="w-16 text-right text-sm text-text-secondary font-body">
                ({{ item.total }})
              </div>
            </div>
          </div>
        </div>

        <!-- Activity by Type -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div class="glass rounded-xl p-6 border border-border-color">
            <h3 class="text-xl font-bold text-text-primary mb-4 font-display">
              Avis par type
            </h3>
            <div class="space-y-3">
              <div
                v-for="(count, type) in statistics.reviews_by_type"
                :key="`review-${type}`"
                class="flex items-center justify-between"
              >
                <span class="text-sm text-text-secondary font-body">
                  {{ getMediaTypeLabel(type) }}
                </span>
                <div class="flex items-center gap-2">
                  <div
                    class="h-2 rounded-full"
                    :style="{ width: `${Math.min(count * 10, 100)}px`, backgroundColor: getMediaTypeHex(type) }"
                  ></div>
                  <span class="text-sm font-bold text-text-primary font-display">{{ count }}</span>
                </div>
              </div>
              <div v-if="Object.keys(statistics.reviews_by_type).length === 0" class="text-sm text-text-tertiary font-body italic">
                Aucun avis pour le moment
              </div>
            </div>
          </div>

          <div class="glass rounded-xl p-6 border border-border-color">
            <h3 class="text-xl font-bold text-text-primary mb-4 font-display">
              Notes par type
            </h3>
            <div class="space-y-3">
              <div
                v-for="(data, type) in statistics.ratings_by_type"
                :key="`rating-${type}`"
                class="space-y-1"
              >
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-text-secondary font-body">
                    {{ getMediaTypeLabel(type) }}
                  </span>
                  <span class="text-sm font-bold text-text-primary font-display">
                    {{ data.average_score.toFixed(1) }}/10
                  </span>
                </div>
                <div class="flex items-center justify-between text-xs text-text-secondary font-body">
                  <span>{{ data.count }} note(s)</span>
                  <div
                    class="h-1.5 rounded-full bg-bg-tertiary flex-1 mx-2 max-w-[100px]"
                  >
                    <div
                      class="h-full rounded-full"
                      :style="{ width: `${(data.average_score / 10) * 100}%`, backgroundColor: getMediaTypeHex(type) }"
                    ></div>
                  </div>
                </div>
              </div>
              <div v-if="Object.keys(statistics.ratings_by_type).length === 0" class="text-sm text-text-tertiary font-body italic">
                Aucune note pour le moment
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Collection View -->
      <div v-if="currentView === 'collection'" class="space-y-6">

        <!-- Filtre par type -->
        <div class="glass rounded-xl p-4 border border-border-color">
          <div class="flex flex-wrap gap-2">
            <button
              v-for="f in mediaTypeFilters"
              :key="f.value ?? 'all'"
              @click="selectedMediaType = f.value"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                selectedMediaType === f.value
                  ? 'bg-accent text-white font-semibold'
                  : 'bg-bg-secondary text-text-secondary hover:bg-bg-tertiary'
              ]"
            >
              {{ f.label }}
            </button>
          </div>
        </div>

        <!-- Chargement initial -->
        <div v-if="collectionLoading" class="flex justify-center py-16">
          <div class="spinner !h-10 !w-10 !border-4"></div>
        </div>

        <!-- Collection vide -->
        <div v-else-if="totalRated === 0" class="glass rounded-xl p-10 border border-border-color text-center">
          <div class="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-bg-tertiary/50 text-4xl">⭐</div>
          <h3 class="mb-2 text-xl font-semibold text-text-primary font-display">Aucun média noté</h3>
          <p class="text-sm text-text-secondary font-body">Notez des films, séries, jeux ou livres pour les voir apparaître ici.</p>
          <NuxtLink to="/explore" class="btn-primary mt-6 inline-block px-6 py-2.5">Parcourir le catalogue</NuxtLink>
        </div>

        <!-- Sections par type -->
        <template v-else>
          <div
            v-for="section in visibleSections"
            :key="section.key"
            class="glass rounded-xl p-6 border border-border-color"
          >
            <div class="mb-5 flex items-center gap-2">
              <span class="text-2xl">{{ section.emoji }}</span>
              <h2 class="text-2xl font-bold text-text-primary font-display">{{ section.label }}</h2>
              <span class="ml-1 rounded-full bg-bg-tertiary px-2.5 py-0.5 text-xs font-semibold text-text-secondary">
                {{ collectionByType[section.key].length }}
              </span>
            </div>

            <div v-if="collectionByType[section.key].length > 0"
              class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
              <div
                v-for="item in collectionByType[section.key]"
                :key="item.media.id"
                class="relative"
              >
                <!-- Badge score utilisateur -->
                <div class="absolute bottom-2 right-2 z-20 flex items-center gap-1 rounded-lg bg-accent px-2 py-1 text-xs font-bold text-white shadow-lg">
                  ★ {{ item.score }}/10
                </div>
                <MediaShow :media="item.media" :hideRating="true" />
              </div>
            </div>

            <div v-else class="py-8 text-center text-sm text-text-tertiary">
              Aucun {{ section.label.toLowerCase() }} noté pour l'instant
            </div>
          </div>
        </template>

      </div> <!-- End Collection View -->

      <!-- Actions -->
      <div class="flex justify-center gap-4">
        <NuxtLink
          to="/"
          class="btn-primary px-6 py-3"
        >
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
