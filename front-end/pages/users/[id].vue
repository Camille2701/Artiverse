<script setup lang="ts">
import type { User } from '~/types/user'
import type { Media } from '~/types/media'
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

const user = ref<User | null>(null)
const error = ref(false)
const userMedia = ref<Media[]>([])
const userReviews = ref<any[]>([])

onMounted(async () => {
  try {
    // Get current user if authenticated
    if (isAuthenticated.value && currentUser.value) {
      user.value = currentUser.value

      // Fetch user's media and reviews
      const [mediaResponse, reviewsResponse] = await Promise.all([
        $fetch('/api/media'),
        $fetch(`/api/v1/users/${user.value.id}/reviews`)
      ])

      userMedia.value = mediaResponse || []
      userReviews.value = reviewsResponse?.items || []
    }
  } catch (e) {
    console.error('Failed to fetch user data:', e)
    error.value = true
  }
})

async function handleLogout() {
  logout()
  await navigateTo('/')
}
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-5xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl sm:text-3xl font-display font-bold text-text-primary">Mon profil</h1>
      <button
        v-if="isAuthenticated"
        @click="handleLogout"
        class="px-4 py-2.5 rounded-xl border-2 border-red-500/30 text-red-400 text-sm font-medium font-display transition-all duration-200 hover:bg-red-500/10 hover:border-red-500/50 hover:text-red-300 sm:text-base"
      >
        Déconnexion
      </button>
    </div>

    <div v-if="error" class="mt-8 glass rounded-xl p-8 text-center border border-red-500/30">
      <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-red-500/20 flex items-center justify-center">
        <span class="text-3xl">⚠️</span>
      </div>
      <h2 class="mb-4 text-xl font-semibold text-red-400 font-display sm:text-2xl">Erreur de chargement</h2>
      <NuxtLink
        to="/"
        class="btn-primary px-6 py-3"
      >
        Retour à l'accueil
      </NuxtLink>
    </div>

    <div v-else-if="user" class="mt-8 space-y-6">
      <!-- Profile Card -->
      <div class="glass rounded-2xl p-6 sm:p-8 border border-white/10">
        <div class="mb-8 flex flex-col items-center gap-6 border-b border-border-color pb-8 text-center sm:flex-row sm:items-center sm:gap-8 sm:text-left">
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-br from-accent-movie via-accent-series to-accent-game rounded-full blur-sm opacity-60"></div>
            <img
              :src="user.avatar_url || 'https://i.pravatar.cc/150?img=12'"
              :alt="user.username"
              class="relative h-28 w-28 sm:h-[120px] sm:w-[120px] lg:h-[130px] lg:w-[130px] rounded-full object-cover border-4 border-bg-secondary"
            />
          </div>
          <div class="flex-1">
            <h2 class="mb-2 text-2xl font-bold text-text-primary font-display sm:text-3xl">{{ user.username }}</h2>
            <p class="mb-4 text-sm text-text-secondary font-body">{{ user.email }}</p>
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

        <div v-if="user.bio" class="mb-4">
          <strong class="mb-2 block text-sm text-text-secondary font-display">À propos</strong>
          <p class="text-text-primary font-body">{{ user.bio }}</p>
        </div>
      </div>

      <!-- Statistics -->
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div class="stat-card">
          <strong class="mb-2 block text-sm text-text-secondary font-display">ID</strong>
          <span class="font-medium text-text-primary font-body">{{ user.id }}</span>
        </div>
        <div class="stat-card">
          <strong class="mb-2 block text-sm text-text-secondary font-display">Nom d'utilisateur</strong>
          <span class="font-medium text-text-primary font-body">{{ user.username }}</span>
        </div>
        <div class="stat-card">
          <strong class="mb-2 block text-sm text-text-secondary font-display">Statut</strong>
          <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-sm font-semibold font-display border border-emerald-500/30">
            ✓ Actif
          </span>
        </div>
      </div>

      <!-- User's Media -->
      <div v-if="userMedia.length > 0">
        <h3 class="mb-4 text-xl font-bold text-text-primary font-display">Mes médias</h3>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <MediaShow
            v-for="media in userMedia"
            :key="media.id"
            :media="media"
          />
        </div>
      </div>

      <!-- User's Reviews -->
      <div v-if="userReviews.length > 0">
        <h3 class="mb-4 text-xl font-bold text-text-primary font-display">Mes avis</h3>
        <div class="space-y-4">
          <div
            v-for="review in userReviews"
            :key="review.id"
            class="discovery-card"
          >
            <h4 class="font-semibold text-text-primary font-display">{{ review.title }}</h4>
            <p class="text-sm text-text-secondary font-body mt-1">{{ review.content }}</p>
            <div class="mt-3 flex gap-3">
              <span class="text-xs text-text-tertiary font-body">{{ new Date(review.created_at).toLocaleDateString('fr-FR') }}</span>
              <span v-if="review.spoiler" class="text-xs text-yellow-400 font-semibold px-2 py-0.5 rounded bg-yellow-500/10 border border-yellow-500/30">⚠️ Spoiler</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-center gap-4 pt-4">
        <NuxtLink
          to="/"
          class="btn-primary px-6 py-3"
        >
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>

    <div v-else-if="!isAuthenticated" class="mt-8 glass rounded-xl p-8 text-center border border-accent/20">
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

    <div v-else class="mt-8 flex flex-col items-center justify-center py-20">
      <div class="spinner !h-12 !w-12 !border-4"></div>
      <p class="mt-4 text-text-secondary font-body">Chargement...</p>
    </div>
  </div>
</template>
