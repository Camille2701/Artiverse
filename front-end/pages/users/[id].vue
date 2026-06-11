<script setup lang="ts">
import type { User } from '~/types/user'
import type { Media } from '~/types/media'
import type { UserStatistics } from '~/types/statistics'
import { MediaType } from '~/types/media'

useHead({
  title: "Artiverse - Profil",
  meta: [
    { name: "Page de consultation d'un utilisateur", content: "Consultation d'un utilisateur"}
  ]
})

const route = useRoute()
const userId = route.params.id as string
const { user: currentUser, isAuthenticated, logout } = useAuth()
const { getTrendingMedia, getAllMedia } = useMedia()
const { getMyStatistics } = useStatistics()
const { getUserRatings } = useRatings()
const { getReviewsByUser } = useReviews()

const user = ref<User | null>(null)
const error = ref(false)
const loading = ref(true)

// Statistics
const statistics = ref<UserStatistics | null>(null)

// View toggle
const currentView = ref<'collection' | 'statistics'>('collection')

// Media sections
const selectedMediaType = ref<string | null>(null)
const trendingMedia = ref<Media[]>([])
const topRatedMedia = ref<Media[]>([])
const userRecentMedia = ref<Media[]>([])
const userTopRatedMedia = ref<Media[]>([])

// Loading states
const loadingMedia = ref({
  trending: false,
  topRated: false,
  recent: false,
  userTopRated: false
})

const mediaTypes = [
  { value: null, label: 'Tous les types' },
  { value: MediaType.Movie, label: 'Films' },
  { value: MediaType.Serie, label: 'Séries' },
  { value: MediaType.Game, label: 'Jeux vidéo' },
  { value: MediaType.Book, label: 'Livres' }
]

onMounted(async () => {
  try {
    // Get current user if authenticated
    if (isAuthenticated.value && currentUser.value) {
      user.value = currentUser.value

      // Fetch user statistics
      try {
        statistics.value = await getMyStatistics()
      } catch (statError) {
        console.error('Failed to fetch statistics:', statError)
      }

      // Load initial media
      await loadAllMedia()
    }
  } catch (e) {
    console.error('Failed to fetch user data:', e)
    error.value = true
  } finally {
    loading.value = false
  }
})

// Watch for media type changes
watch(selectedMediaType, () => {
  loadAllMedia()
})

async function loadAllMedia() {
  await Promise.all([
    loadTrendingMedia(),
    loadTopRatedMedia(),
    loadUserRecentMedia(),
    loadUserTopRatedMedia()
  ])
}

async function loadTrendingMedia() {
  try {
    loadingMedia.value.trending = true
    const params = selectedMediaType.value ? { limit: 8, media_type: selectedMediaType.value } : { limit: 8 }
    trendingMedia.value = await getTrendingMedia(params)
  } catch (error) {
    console.error('Failed to load trending media:', error)
    trendingMedia.value = []
  } finally {
    loadingMedia.value.trending = false
  }
}

async function loadTopRatedMedia() {
  try {
    loadingMedia.value.topRated = true
    const params = selectedMediaType.value
      ? { limit: 8, media_type: selectedMediaType.value, sort_by: 'rating', order: 'desc' }
      : { limit: 8, sort_by: 'rating', order: 'desc' }
    const response = await getAllMedia(params)
    topRatedMedia.value = response.items || []
  } catch (error) {
    console.error('Failed to load top rated media:', error)
    topRatedMedia.value = []
  } finally {
    loadingMedia.value.topRated = false
  }
}

async function loadUserRecentMedia() {
  try {
    loadingMedia.value.recent = true

    if (!isAuthenticated.value || !currentUser.value) {
      userRecentMedia.value = []
      return
    }

    // Get user's recent reviews to determine recently interacted media
    const reviewsResponse = await getReviewsByUser(currentUser.value.id, { limit: 20 })

    if (!reviewsResponse?.items || reviewsResponse.items.length === 0) {
      userRecentMedia.value = []
      return
    }

    // Get unique media IDs from reviews
    const mediaIds = [...new Set(reviewsResponse.items.map(review => review.media_id))]

    // Fetch full media objects
    const mediaPromises = mediaIds.map(id =>
      $fetch<Media>(`/api/v1/media/${id}`).catch(() => null)
    )
    const mediaItems = await Promise.all(mediaPromises)
    let allRecentMedia = mediaItems.filter((m): m is Media => m !== null)

    // Sort by review date (most recent first)
    allRecentMedia.sort((a, b) => {
      const aReview = reviewsResponse.items.find(r => r.media_id === a.id)
      const bReview = reviewsResponse.items.find(r => r.media_id === b.id)
      const aDate = aReview ? new Date(aReview.created_at).getTime() : 0
      const bDate = bReview ? new Date(bReview.created_at).getTime() : 0
      return bDate - aDate
    })

    // Filter by selected media type if needed
    if (selectedMediaType.value) {
      userRecentMedia.value = allRecentMedia.filter(
        m => m.media_type === selectedMediaType.value
      )
    } else {
      userRecentMedia.value = allRecentMedia.slice(0, 8)
    }
  } catch (error) {
    console.error('Failed to load user recent media:', error)
    userRecentMedia.value = []
  } finally {
    loadingMedia.value.recent = false
  }
}

async function loadUserTopRatedMedia() {
  try {
    loadingMedia.value.userTopRated = true

    if (!isAuthenticated.value || !currentUser.value) {
      userTopRatedMedia.value = []
      return
    }

    // Get user's ratings to determine top rated media
    const ratingsResponse = await getUserRatings({ limit: 50 })

    if (!ratingsResponse?.items || ratingsResponse.items.length === 0) {
      userTopRatedMedia.value = []
      return
    }

    // Filter for ratings 8+ (top rated)
    const topRatedRatings = ratingsResponse.items.filter(rating => rating.score >= 8)

    // Get unique media IDs from ratings
    const mediaIds = [...new Set(topRatedRatings.map(rating => rating.media_id))]

    // Fetch full media objects
    const mediaPromises = mediaIds.map(id =>
      $fetch<Media>(`/api/v1/media/${id}`).catch(() => null)
    )
    const mediaItems = await Promise.all(mediaPromises)
    let allTopRated = mediaItems.filter((m): m is Media => m !== null)

    // Sort by rating score (highest first)
    allTopRated.sort((a, b) => {
      const aRating = topRatedRatings.find(r => r.media_id === a.id)
      const bRating = topRatedRatings.find(r => r.media_id === b.id)
      const aScore = aRating ? aRating.score : 0
      const bScore = bRating ? bRating.score : 0
      return bScore - aScore
    })

    // Filter by selected media type if needed
    if (selectedMediaType.value) {
      userTopRatedMedia.value = allTopRated.filter(
        m => m.media_type === selectedMediaType.value
      )
    } else {
      userTopRatedMedia.value = allTopRated.slice(0, 8)
    }
  } catch (error) {
    console.error('Failed to load user top rated media:', error)
    userTopRatedMedia.value = []
  } finally {
    loadingMedia.value.userTopRated = false
  }
}

function getMediaTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    'movie': 'Films',
    'tv_series': 'Séries',
    'video_game': 'Jeux vidéo',
    'book': 'Livres'
  }
  return labels[type] || type
}

function getMediaTypeColor(type: string): string {
  const colors: Record<string, string> = {
    'movie': 'media-movie',
    'tv_series': 'media-series',
    'video_game': 'media-game',
    'book': 'media-book'
  }
  return colors[type] || ''
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
            <div class="flex flex-wrap gap-3">
              <span class="px-4 py-1.5 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 text-white text-sm font-semibold font-display">
                Niveau {{ user.level }}
              </span>
              <span class="px-4 py-1.5 rounded-full bg-gradient-to-r from-purple-500 to-purple-600 text-white text-sm font-semibold font-display">
                {{ user.experience_points }} XP
              </span>
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
                    :class="getMediaTypeColor(type)"
                    :style="{ width: `${item.percentage}%` }"
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
                    :class="getMediaTypeColor(type)"
                    :style="{ width: `${Math.min(count * 10, 100)}px` }"
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
                      :class="getMediaTypeColor(type)"
                      :style="{ width: `${(data.average_score / 10) * 100}%` }"
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
      <div v-if="currentView === 'collection'">

      <!-- Media Type Filter (Collection View Only) -->
      <div v-if="currentView === 'collection'" class="glass rounded-xl p-4 border border-border-color">
        <label class="block text-sm font-medium text-text-primary mb-3 font-display">Filtrer par type de média</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="type in mediaTypes"
            :key="type.value || 'all'"
            @click="selectedMediaType = type.value"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
              selectedMediaType === type.value
                ? 'bg-accent text-white font-semibold'
                : 'bg-bg-secondary text-text-secondary hover:bg-bg-tertiary'
            ]"
          >
            {{ type.label }}
          </button>
        </div>
      </div>

      <!-- Trending Media Section -->
      <div v-if="currentView === 'collection'" class="glass rounded-xl p-6 border border-border-color">
        <h2 class="text-2xl font-bold text-text-primary mb-4 font-display flex items-center gap-2">
          <span class="text-2xl">🔥</span>
          Top Trending
          <span v-if="selectedMediaType" class="text-sm font-normal text-text-secondary">
            ({{ getMediaTypeLabel(selectedMediaType) }})
          </span>
        </h2>
        <div v-if="loadingMedia.trending" class="flex justify-center py-8">
          <div class="spinner !h-8 !w-8 !border-3"></div>
        </div>
        <div v-else-if="trendingMedia.length > 0" class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          <MediaCard
            v-for="media in trendingMedia"
            :key="media.id"
            :media="media"
          />
        </div>
        <div v-else class="text-center py-8 text-text-secondary">
          Aucun média trending disponible
        </div>
      </div>

      <!-- Top Rated Media Section -->
      <div class="glass rounded-xl p-6 border border-border-color">
        <h2 class="text-2xl font-bold text-text-primary mb-4 font-display flex items-center gap-2">
          <span class="text-2xl">⭐</span>
          Top Notés
          <span v-if="selectedMediaType" class="text-sm font-normal text-text-secondary">
            ({{ getMediaTypeLabel(selectedMediaType) }})
          </span>
        </h2>
        <div v-if="loadingMedia.topRated" class="flex justify-center py-8">
          <div class="spinner !h-8 !w-8 !border-3"></div>
        </div>
        <div v-else-if="topRatedMedia.length > 0" class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          <MediaCard
            v-for="media in topRatedMedia"
            :key="media.id"
            :media="media"
          />
        </div>
        <div v-else class="text-center py-8 text-text-secondary">
          Aucun média noté disponible
        </div>
      </div>

      <!-- User Recent Media Section -->
      <div class="glass rounded-xl p-6 border border-border-color">
        <h2 class="text-2xl font-bold text-text-primary mb-4 font-display flex items-center gap-2">
          <span class="text-2xl">🕐</span>
          Récemment ajoutés
          <span v-if="selectedMediaType" class="text-sm font-normal text-text-secondary">
            ({{ getMediaTypeLabel(selectedMediaType) }})
          </span>
        </h2>
        <div v-if="loadingMedia.recent" class="flex justify-center py-8">
          <div class="spinner !h-8 !w-8 !border-3"></div>
        </div>
        <div v-else-if="userRecentMedia.length > 0" class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          <MediaCard
            v-for="media in userRecentMedia"
            :key="media.id"
            :media="media"
          />
        </div>
        <div v-else class="text-center py-8 text-text-secondary">
          Aucun média récent disponible
        </div>
      </div>

      <!-- User Top Rated Media Section -->
      <div v-if="statistics && statistics.top_rated && statistics.top_rated.length > 0" class="glass rounded-xl p-6 border border-border-color">
        <h2 class="text-2xl font-bold text-text-primary mb-4 font-display flex items-center gap-2">
          <span class="text-2xl">💖</span>
          Mes coups de cœur
          <span v-if="selectedMediaType" class="text-sm font-normal text-text-secondary">
            ({{ getMediaTypeLabel(selectedMediaType) }})
          </span>
        </h2>
        <div v-if="loadingMedia.userTopRated" class="flex justify-center py-8">
          <div class="spinner !h-8 !w-8 !border-3"></div>
        </div>
        <div v-else-if="userTopRatedMedia.length > 0" class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          <MediaCard
            v-for="media in userTopRatedMedia"
            :key="media.id"
            :media="media"
          />
        </div>
        <div v-else class="text-center py-8 text-text-secondary">
          Aucun coup de cœur disponible pour ce type
        </div>
      </div>
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
