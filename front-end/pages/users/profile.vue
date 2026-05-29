<template>
  <div class="max-w-6xl mx-auto">
    <div class="mb-6">
      <h1 class="text-3xl font-display font-bold text-text-primary">Mon Profil</h1>
      <p class="text-text-secondary mt-2 font-body">Gérez votre identité culturelle et découvrez vos statistiques</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <div class="spinner"></div>
      <p class="mt-4 text-text-secondary font-body">Chargement de votre profil...</p>
    </div>

    <!-- Error / not authenticated -->
    <div v-else-if="loadError" class="card p-6 border-l-4 border-l-red-500">
      <h3 class="text-lg font-semibold text-red-400">Erreur de chargement</h3>
      <p class="mt-2 text-sm text-text-secondary">{{ loadError }}</p>
      <NuxtLink to="/users/login" class="mt-4 inline-block btn-primary text-sm px-4 py-2">
        Se connecter
      </NuxtLink>
    </div>

    <!-- Profile -->
    <UserProfile
      v-else-if="profileUser"
      :user="profileUser"
      :stats="stats"
      :badges="badges"
      :favorite-media="favoriteMedia"
      :recent-activity="recentActivity"
    />
  </div>
</template>

<script setup lang="ts">
import UserProfile from '~/components/UserProfile.vue'
import { useApi } from '~/composables/useApi'

const { fetchWithAuth, getErrorMessage } = useApi()

const profileUser = ref<any>(null)
const stats = ref({ movies: 0, series: 0, games: 0, books: 0 })
const badges = ref<any[]>([])
const favoriteMedia = ref<any[]>([])
const recentActivity = ref<any[]>([])
const loading = ref(true)
const loadError = ref('')

const ACTIVITY_META: Record<string, { icon: string; title: string }> = {
  review_created: { icon: '📝', title: 'Critique publiée' },
  rating_given: { icon: '⭐', title: 'Note donnée' },
  list_created: { icon: '📋', title: 'Liste créée' },
  media_added_to_list: { icon: '➕', title: 'Média ajouté à une liste' },
  badge_earned: { icon: '🏅', title: 'Badge débloqué' },
  level_up: { icon: '🚀', title: 'Niveau supérieur' },
}

async function loadProfile() {
  loading.value = true
  loadError.value = ''
  try {
    const me: any = await fetchWithAuth('/api/v1/users/me')
    profileUser.value = {
      id: me.id,
      username: me.username,
      email: me.email,
      avatar: me.avatar_url || undefined,
      bio: me.bio || undefined,
      level: me.level,
      experiencePoints: me.experience_points,
    }

    const [statData, badgeData, activityData]: any[] = await Promise.all([
      fetchWithAuth(`/api/v1/statistics/users/${me.id}`),
      fetchWithAuth('/api/v1/badges/my-badges').catch(() => []),
      fetchWithAuth(`/api/v1/social/activity/${me.id}`).catch(() => ({ activity: [] })),
    ])

    const td = statData?.taste_distribution || {}
    stats.value = {
      movies: td.movie?.total || 0,
      series: td.tv_series?.total || 0,
      games: td.video_game?.total || 0,
      books: td.book?.total || 0,
    }

    favoriteMedia.value = (statData?.top_rated || []).map((m: any) => ({
      id: m.media_id,
      title: m.title,
      image: m.cover_image || undefined,
      type: m.media_type,
    }))

    badges.value = (badgeData || []).map((b: any) => ({
      id: b.id,
      name: b.name,
      description: b.description,
      icon: b.icon || '🏅',
      level: b.tier,
      style: b.tier,
    }))

    recentActivity.value = (activityData?.activity || []).map((a: any) => {
      const meta = ACTIVITY_META[a.activity_type] || { icon: '•', title: a.activity_type }
      const mediaTitle = a.media?.title
      return {
        id: a.id,
        icon: meta.icon,
        title: meta.title,
        description: mediaTitle ? `${meta.title} — « ${mediaTitle} »` : meta.title,
        date: a.created_at,
      }
    })
  } catch (err: any) {
    loadError.value = getErrorMessage(err)
  } finally {
    loading.value = false
  }
}

onMounted(loadProfile)
</script>
