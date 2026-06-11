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
const { isDark } = useTheme()

const user = ref<User | null>(null)
const error = ref(false)
const loading = ref(true)

const statistics = ref<UserStatistics | null>(null)
const currentView = ref<'collection' | 'statistics' | 'badges'>('collection')
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

// --- Badge definitions ---
interface Badge {
  id: string
  emoji: string
  name: string
  description: string
  color: string
  earned: boolean
  progress?: { current: number; target: number }
}

const BADGE_DEFS = [
  // ── Premiers pas ──────────────────────────────────────────────────────────
  { id: 'first_rating',      emoji: '⭐', name: 'Premier pas',        description: 'Notez votre premier média',                                color: '#22c55e', check: (s: any) => s.total_ratings >= 1 },
  { id: 'first_review',      emoji: '✍️', name: 'Critique en herbe',  description: 'Rédigez votre premier avis',                               color: '#3b82f6', check: (s: any) => s.total_reviews >= 1 },
  { id: 'first_list',        emoji: '📋', name: 'Organisateur',       description: 'Créez votre première liste',                               color: '#06b6d4', check: (s: any) => s.total_lists >= 1 },

  // ── Paliers de notes (quantité globale) ───────────────────────────────────
  { id: 'ratings_10',        emoji: '🌟', name: 'Collectionneur',     description: 'Notez 10 médias',   color: '#f59e0b', check: (s: any) => s.total_ratings >= 10,  prog: (s: any) => ({ current: Math.min(s.total_ratings, 10),  target: 10  }) },
  { id: 'ratings_25',        emoji: '🎯', name: 'Vingtaine',          description: 'Notez 25 médias',   color: '#fb923c', check: (s: any) => s.total_ratings >= 25,  prog: (s: any) => ({ current: Math.min(s.total_ratings, 25),  target: 25  }) },
  { id: 'ratings_50',        emoji: '💎', name: 'Connaisseur',        description: 'Notez 50 médias',   color: '#a855f7', check: (s: any) => s.total_ratings >= 50,  prog: (s: any) => ({ current: Math.min(s.total_ratings, 50),  target: 50  }) },
  { id: 'ratings_100',       emoji: '🏆', name: 'Centurion',          description: 'Notez 100 médias',  color: '#f59e0b', check: (s: any) => s.total_ratings >= 100, prog: (s: any) => ({ current: Math.min(s.total_ratings, 100), target: 100 }) },
  { id: 'ratings_200',       emoji: '👑', name: 'Légende',            description: 'Notez 200 médias',  color: '#fbbf24', check: (s: any) => s.total_ratings >= 200, prog: (s: any) => ({ current: Math.min(s.total_ratings, 200), target: 200 }) },

  // ── Films ─────────────────────────────────────────────────────────────────
  { id: 'movie_5',           emoji: '🎬', name: 'Cinéphile',          description: 'Notez 5 films',    color: '#FF4757', check: (s: any) => (s.ratings_by_type?.movie?.count ?? 0) >= 5,  prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.movie?.count ?? 0, 5),  target: 5  }) },
  { id: 'movie_20',          emoji: '🎥', name: 'Grand cinéphile',    description: 'Notez 20 films',   color: '#ef4444', check: (s: any) => (s.ratings_by_type?.movie?.count ?? 0) >= 20, prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.movie?.count ?? 0, 20), target: 20 }) },
  { id: 'movie_50',          emoji: '🏛️', name: 'Cinémathèque',       description: 'Notez 50 films',   color: '#dc2626', check: (s: any) => (s.ratings_by_type?.movie?.count ?? 0) >= 50, prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.movie?.count ?? 0, 50), target: 50 }) },

  // ── Séries ────────────────────────────────────────────────────────────────
  { id: 'series_5',          emoji: '📺', name: 'Sériephile',         description: 'Notez 5 séries',   color: '#9B51E0', check: (s: any) => (s.ratings_by_type?.tv_series?.count ?? 0) >= 5,  prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.tv_series?.count ?? 0, 5),  target: 5  }) },
  { id: 'series_20',         emoji: '📡', name: 'Accro aux séries',   description: 'Notez 20 séries',  color: '#7c3aed', check: (s: any) => (s.ratings_by_type?.tv_series?.count ?? 0) >= 20, prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.tv_series?.count ?? 0, 20), target: 20 }) },
  { id: 'series_50',         emoji: '🎭', name: 'Marathonien',        description: 'Notez 50 séries',  color: '#6d28d9', check: (s: any) => (s.ratings_by_type?.tv_series?.count ?? 0) >= 50, prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.tv_series?.count ?? 0, 50), target: 50 }) },

  // ── Jeux vidéo ────────────────────────────────────────────────────────────
  { id: 'game_5',            emoji: '🎮', name: 'Gamer',              description: 'Notez 5 jeux vidéo',    color: '#00D2D3', check: (s: any) => (s.ratings_by_type?.video_game?.count ?? 0) >= 5,  prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.video_game?.count ?? 0, 5),  target: 5  }) },
  { id: 'game_20',           emoji: '🕹️', name: 'Hardcore gamer',     description: 'Notez 20 jeux vidéo',   color: '#0891b2', check: (s: any) => (s.ratings_by_type?.video_game?.count ?? 0) >= 20, prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.video_game?.count ?? 0, 20), target: 20 }) },
  { id: 'game_50',           emoji: '🏅', name: 'Pro gamer',          description: 'Notez 50 jeux vidéo',   color: '#0e7490', check: (s: any) => (s.ratings_by_type?.video_game?.count ?? 0) >= 50, prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.video_game?.count ?? 0, 50), target: 50 }) },

  // ── Livres ────────────────────────────────────────────────────────────────
  { id: 'book_5',            emoji: '📚', name: 'Bibliophile',        description: 'Notez 5 livres',    color: '#ECCC68', check: (s: any) => (s.ratings_by_type?.book?.count ?? 0) >= 5,  prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.book?.count ?? 0, 5),  target: 5  }) },
  { id: 'book_20',           emoji: '📖', name: 'Rat de biblio',      description: 'Notez 20 livres',   color: '#ca8a04', check: (s: any) => (s.ratings_by_type?.book?.count ?? 0) >= 20, prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.book?.count ?? 0, 20), target: 20 }) },
  { id: 'book_50',           emoji: '🗝️', name: 'Archiviste',         description: 'Notez 50 livres',   color: '#a16207', check: (s: any) => (s.ratings_by_type?.book?.count ?? 0) >= 50, prog: (s: any) => ({ current: Math.min(s.ratings_by_type?.book?.count ?? 0, 50), target: 50 }) },

  // ── Diversité ────────────────────────────────────────────────────────────
  { id: 'eclectic_1',        emoji: '🌈', name: 'Éclectique',         description: 'Notez au moins 1 média de chaque type',  color: '#ec4899', check: (s: any) => ['movie','tv_series','video_game','book'].every((t: string) => (s.ratings_by_type?.[t]?.count ?? 0) >= 1) },
  { id: 'eclectic_5',        emoji: '🌍', name: 'Omnivore',           description: 'Notez 5 médias de chaque type',           color: '#db2777', check: (s: any) => ['movie','tv_series','video_game','book'].every((t: string) => (s.ratings_by_type?.[t]?.count ?? 0) >= 5), prog: (s: any) => ({ current: Math.min(...(['movie','tv_series','video_game','book'].map((t: string) => s.ratings_by_type?.[t]?.count ?? 0))), target: 5 }) },

  // ── Avis ─────────────────────────────────────────────────────────────────
  { id: 'reviews_5',         emoji: '🏅', name: 'Critique confirmé',  description: 'Rédigez 5 avis',   color: '#6366f1', check: (s: any) => s.total_reviews >= 5,  prog: (s: any) => ({ current: Math.min(s.total_reviews, 5),  target: 5  }) },
  { id: 'reviews_15',        emoji: '🖊️', name: 'Plume d\'or',        description: 'Rédigez 15 avis',  color: '#4f46e5', check: (s: any) => s.total_reviews >= 15, prog: (s: any) => ({ current: Math.min(s.total_reviews, 15), target: 15 }) },
  { id: 'reviews_30',        emoji: '📝', name: 'Grand rédacteur',    description: 'Rédigez 30 avis',  color: '#4338ca', check: (s: any) => s.total_reviews >= 30, prog: (s: any) => ({ current: Math.min(s.total_reviews, 30), target: 30 }) },

  // ── Listes ────────────────────────────────────────────────────────────────
  { id: 'lists_3',           emoji: '🗂️', name: 'Curateur',           description: 'Créez 3 listes',                        color: '#0ea5e9', check: (s: any) => s.total_lists >= 3, prog: (s: any) => ({ current: Math.min(s.total_lists, 3), target: 3 }) },
  { id: 'lists_5',           emoji: '🗃️', name: 'Gestionnaire',       description: 'Créez 5 listes',                        color: '#0284c7', check: (s: any) => s.total_lists >= 5, prog: (s: any) => ({ current: Math.min(s.total_lists, 5), target: 5 }) },
  { id: 'list_items_20',     emoji: '📦', name: 'Grande collection',  description: 'Ajoutez 20 médias dans vos listes',      color: '#0369a1', check: (s: any) => s.total_media_in_lists >= 20,  prog: (s: any) => ({ current: Math.min(s.total_media_in_lists, 20),  target: 20  }) },
  { id: 'list_items_100',    emoji: '🏰', name: 'Grande bibliothèque',description: 'Ajoutez 100 médias dans vos listes',     color: '#075985', check: (s: any) => s.total_media_in_lists >= 100, prog: (s: any) => ({ current: Math.min(s.total_media_in_lists, 100), target: 100 }) },

  // ── Streak ────────────────────────────────────────────────────────────────
  { id: 'streak_3',          emoji: '🔥', name: 'Sur la lancée',      description: '3 jours de connexion consécutifs',   color: '#f97316', check: (_: any, u: any) => (u?.streak_days ?? 0) >= 3 },
  { id: 'streak_7',          emoji: '💫', name: 'Semaine parfaite',   description: '7 jours de connexion consécutifs',   color: '#f59e0b', check: (_: any, u: any) => (u?.streak_days ?? 0) >= 7  },
  { id: 'streak_30',         emoji: '☀️', name: 'Mois de feu',        description: '30 jours de connexion consécutifs',  color: '#eab308', check: (_: any, u: any) => (u?.streak_days ?? 0) >= 30 },

  // ── Niveau XP ─────────────────────────────────────────────────────────────
  { id: 'level_2',           emoji: '🌱', name: 'Débutant',           description: 'Atteignez le niveau 2',  color: '#22c55e', check: (_: any, u: any) => (u?.level ?? 1) >= 2  },
  { id: 'level_5',           emoji: '💪', name: 'Intermédiaire',      description: 'Atteignez le niveau 5',  color: '#3b82f6', check: (_: any, u: any) => (u?.level ?? 1) >= 5  },
  { id: 'level_10',          emoji: '🔮', name: 'Expert',             description: 'Atteignez le niveau 10', color: '#a855f7', check: (_: any, u: any) => (u?.level ?? 1) >= 10 },
  { id: 'level_20',          emoji: '🌌', name: 'Maître',             description: 'Atteignez le niveau 20', color: '#7c3aed', check: (_: any, u: any) => (u?.level ?? 1) >= 20 },

  // ── Qualité des notes ─────────────────────────────────────────────────────
  { id: 'high_avg',          emoji: '🎖️', name: 'Note généreuse',     description: 'Moyenne ≥ 8/10 sur 10 notes minimum',  color: '#f59e0b', check: (s: any) => s.total_ratings >= 10 && overallAvg(s) >= 8 },
  { id: 'strict_rater',      emoji: '🧐', name: 'Critique exigeant',  description: 'Moyenne ≤ 5/10 sur 10 notes minimum',  color: '#94a3b8', check: (s: any) => s.total_ratings >= 10 && overallAvg(s) <= 5 },
  { id: 'balanced_rater',    emoji: '⚖️', name: 'Équilibré',          description: 'Moyenne entre 6 et 7 sur 10 notes min',color: '#64748b', check: (s: any) => s.total_ratings >= 10 && overallAvg(s) > 5 && overallAvg(s) < 8 },

  // ── Spéciaux ──────────────────────────────────────────────────────────────
  { id: 'all_types_10',      emoji: '🦋', name: 'Papillon culturel',  description: 'Notez 10 médias de chaque type',     color: '#e879f9', check: (s: any) => ['movie','tv_series','video_game','book'].every((t: string) => (s.ratings_by_type?.[t]?.count ?? 0) >= 10), prog: (s: any) => ({ current: Math.min(...(['movie','tv_series','video_game','book'].map((t: string) => s.ratings_by_type?.[t]?.count ?? 0))), target: 10 }) },
  { id: 'polyglotte',        emoji: '🔭', name: 'Explorateur',        description: 'Plus de médias notés que de jours depuis l\'inscription', color: '#0ea5e9', check: (s: any) => s.total_ratings >= 30 },
  { id: 'top_rated_3',       emoji: '💯', name: 'Coup de cœur',       description: 'Donnez 3 notes de 10/10',             color: '#ef4444', check: (s: any) => (s.top_rated?.filter((m: any) => m.rating === 10)?.length ?? 0) >= 3 },
]

function overallAvg(s: any): number {
  let total = 0, count = 0
  for (const t of ['movie', 'tv_series', 'video_game', 'book']) {
    const d = s.ratings_by_type?.[t]
    if (d?.count) { total += d.average_score * d.count; count += d.count }
  }
  return count ? total / count : 0
}

const badges = computed<Badge[]>(() => {
  const stats = statistics.value
  if (!stats) return BADGE_DEFS.map(d => ({ ...d, earned: false }))
  return BADGE_DEFS.map(d => ({
    id: d.id,
    emoji: d.emoji,
    name: d.name,
    description: d.description,
    color: d.color,
    earned: d.check(stats, user.value),
    progress: d.prog ? d.prog(stats) : undefined,
  }))
})

const earnedBadges = computed(() => badges.value.filter(b => b.earned))
const lockedBadges = computed(() => badges.value.filter(b => !b.earned))

// --- Activity chart (last 30 days) ---
const activityDays = computed(() => {
  const result: { label: string; count: number; date: string }[] = []
  if (!statistics.value?.activity_timeline) return result
  const today = new Date()
  for (let i = 29; i >= 0; i--) {
    const d = new Date(today)
    d.setDate(d.getDate() - i)
    const key = d.toISOString().split('T')[0]
    result.push({
      date: key,
      label: d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' }),
      count: statistics.value.activity_timeline[key] ?? 0,
    })
  }
  return result
})

const maxActivityCount = computed(() =>
  Math.max(1, ...activityDays.value.map(d => d.count))
)

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
            <div class="flex flex-wrap items-center gap-3 mb-2">
              <h1 class="text-3xl font-bold text-text-primary font-display sm:text-4xl">{{ user.username }}</h1>
              <span v-if="user.streak_days && user.streak_days >= 2" class="flex items-center gap-1 rounded-full px-3 py-1 text-sm font-semibold" style="background: rgba(249,115,22,0.15); color: #f97316; border: 1px solid rgba(249,115,22,0.3)">
                🔥 {{ user.streak_days }} jours
              </span>
            </div>
            <p v-if="user.bio" class="mb-4 text-text-secondary font-body">{{ user.bio }}</p>
            <!-- XP progress bar -->
            <div class="w-full max-w-sm">
              <div class="flex justify-between text-xs text-text-tertiary mb-1.5">
                <span class="font-semibold text-text-secondary">Niv. {{ user.level }}</span>
                <span>{{ user.experience_points }} / {{ 100 * user.level ** 2 }} XP</span>
                <span class="font-semibold text-text-secondary">Niv. {{ user.level + 1 }}</span>
              </div>
              <div class="h-2.5 w-full rounded-full overflow-hidden" :style="{ background: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(26,24,32,0.08)' }">
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
      <div v-if="statistics" class="grid grid-cols-2 gap-4 sm:grid-cols-5">
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
        <div class="stat-card text-center col-span-2 sm:col-span-1">
          <div class="text-3xl sm:text-4xl font-extrabold font-display" style="color: #f59e0b">{{ earnedBadges.length }}/{{ badges.length }}</div>
          <div class="mt-2 text-sm font-medium text-text-secondary font-body">Succès</div>
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
            <button
              @click="currentView = 'badges'"
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-all duration-200',
                currentView === 'badges'
                  ? 'bg-accent text-white shadow-lg'
                  : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
              ]"
            >
              Succès
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
        <!-- Activity Timeline -->
        <div class="glass rounded-xl p-6 border border-border-color">
          <h3 class="text-xl font-bold text-text-primary mb-4 font-display">Activité (30 derniers jours)</h3>
          <div v-if="activityDays.some(d => d.count > 0)" class="flex items-end gap-1 h-24">
            <div
              v-for="day in activityDays"
              :key="day.date"
              class="flex-1 flex flex-col items-center justify-end"
              :title="`${day.label} : ${day.count} action(s)`"
            >
              <div
                class="w-full rounded-t-sm transition-all duration-300"
                :style="{
                  height: `${Math.max(4, (day.count / maxActivityCount) * 80)}px`,
                  background: day.count > 0
                    ? 'linear-gradient(to top, #3b82f6, #a855f7)'
                    : (isDark ? 'rgba(255,255,255,0.05)' : 'rgba(26,24,32,0.07)')
                }"
              ></div>
            </div>
          </div>
          <div v-else class="flex h-24 items-center justify-center text-sm text-text-tertiary font-body italic">
            Aucune activité ces 30 derniers jours
          </div>
          <div class="mt-2 flex justify-between text-xs text-text-tertiary font-body">
            <span>{{ activityDays[0]?.label }}</span>
            <span>Aujourd'hui</span>
          </div>
        </div>

        <!-- Top Rated -->
        <div v-if="statistics.top_rated?.length" class="glass rounded-xl p-6 border border-border-color">
          <h3 class="text-xl font-bold text-text-primary mb-4 font-display">Vos coups de cœur</h3>
          <div class="space-y-3">
            <div
              v-for="item in statistics.top_rated"
              :key="item.media_id"
              class="flex items-center gap-3"
            >
              <NuxtLink :to="`/media/${item.media_id}`" class="flex items-center gap-3 flex-1 min-w-0 group">
                <div
                  class="h-10 w-10 rounded-lg flex items-center justify-center shrink-0 text-lg font-bold"
                  :style="{ background: getMediaTypeHex(item.media_type) + '22', color: getMediaTypeHex(item.media_type) }"
                >
                  {{ item.media_type === 'movie' ? '🎬' : item.media_type === 'tv_series' ? '📺' : item.media_type === 'video_game' ? '🎮' : '📚' }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-semibold text-text-primary truncate group-hover:text-accent transition-colors">{{ item.title }}</div>
                  <div class="text-xs text-text-tertiary">{{ getMediaTypeLabel(item.media_type) }}</div>
                </div>
              </NuxtLink>
              <div class="shrink-0 rounded-lg px-2.5 py-1 text-sm font-bold" style="background: rgba(245,158,11,0.15); color: #f59e0b">
                ★ {{ item.rating }}/10
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Badges / Succès View -->
      <div v-if="currentView === 'badges'" class="space-y-6">
        <!-- Earned badges -->
        <div class="glass rounded-xl p-6 border border-border-color">
          <h3 class="text-xl font-bold text-text-primary mb-1 font-display">
            Succès débloqués
            <span class="ml-2 text-base font-semibold" style="color: #f59e0b">{{ earnedBadges.length }}/{{ badges.length }}</span>
          </h3>
          <p class="text-sm text-text-tertiary mb-5 font-body">Vos accomplissements sur Artiverse</p>
          <div v-if="earnedBadges.length" class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
            <div
              v-for="badge in earnedBadges"
              :key="badge.id"
              class="rounded-xl p-4 text-center transition-all duration-200 hover:scale-105"
              :style="{ background: badge.color + '18', border: `1px solid ${badge.color}44` }"
            >
              <div class="text-3xl mb-2">{{ badge.emoji }}</div>
              <div class="text-sm font-bold text-text-primary font-display">{{ badge.name }}</div>
              <div class="text-xs text-text-tertiary mt-1 font-body">{{ badge.description }}</div>
            </div>
          </div>
          <div v-else class="py-8 text-center text-sm text-text-tertiary font-body italic">
            Commencez à noter des médias pour débloquer vos premiers succès !
          </div>
        </div>

        <!-- Locked badges -->
        <div v-if="lockedBadges.length" class="glass rounded-xl p-6 border border-border-color">
          <h3 class="text-xl font-bold text-text-primary mb-5 font-display">Succès à débloquer</h3>
          <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
            <div
              v-for="badge in lockedBadges"
              :key="badge.id"
              class="rounded-xl p-4 text-center opacity-50"
              :style="{ background: isDark ? 'rgba(255,255,255,0.04)' : 'rgba(26,24,32,0.03)', border: isDark ? '1px solid rgba(255,255,255,0.08)' : '1px solid rgba(26,24,32,0.08)' }"
            >
              <div class="text-3xl mb-2 grayscale">{{ badge.emoji }}</div>
              <div class="text-sm font-bold text-text-primary font-display">{{ badge.name }}</div>
              <div class="text-xs text-text-tertiary mt-1 font-body">{{ badge.description }}</div>
              <div v-if="badge.progress" class="mt-2">
                <div class="h-1.5 w-full rounded-full overflow-hidden" :style="{ background: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(26,24,32,0.09)' }">
                  <div
                    class="h-full rounded-full"
                    :style="{ background: isDark ? 'rgba(255,255,255,0.3)' : 'rgba(26,24,32,0.2)', width: `${(badge.progress.current / badge.progress.target) * 100}%` }"
                  ></div>
                </div>
                <div class="text-xs text-text-tertiary mt-1 font-body">{{ badge.progress.current }}/{{ badge.progress.target }}</div>
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
