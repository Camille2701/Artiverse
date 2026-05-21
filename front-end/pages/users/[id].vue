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
      <h1 class="text-2xl font-semibold text-slate-900 dark:text-text-primary sm:text-3xl">Mon profil</h1>
      <button
        v-if="isAuthenticated"
        @click="handleLogout"
        class="rounded-md border border-red-300 px-4 py-2 text-sm font-medium text-red-600 transition-all duration-200 ease-out hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1 sm:text-base dark:border-red-800 dark:text-red-400 dark:hover:bg-red-900/20 dark:focus:ring-red-600 dark:focus:ring-offset-bg-secondary"
      >
        Déconnexion
      </button>
    </div>

    <div v-if="error" class="mt-4 p-4 text-center sm:mt-6 sm:p-6 lg:mt-8 lg:p-8">
      <h2 class="mb-4 text-xl font-semibold text-red-500 sm:text-2xl dark:text-red-400">Erreur de chargement</h2>
      <NuxtLink
        to="/"
        class="inline-block rounded-md bg-slate-600 px-5 py-2.5 text-sm font-semibold text-white transition-all duration-200 ease-out hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-1 active:bg-slate-800 sm:px-6 sm:py-3 sm:text-base dark:bg-slate-700 dark:hover:bg-slate-600 dark:focus:ring-slate-600 dark:focus:ring-offset-bg-secondary"
      >
        Retour à l'accueil
      </NuxtLink>
    </div>

    <div v-else-if="user" class="mt-4 space-y-6 sm:mt-6 lg:mt-8">
      <!-- Profile Card -->
      <div class="rounded-xl bg-white p-4 shadow-md sm:p-6 lg:p-8 dark:bg-bg-secondary dark:shadow-lg/20">
        <div class="mb-6 flex flex-col items-center gap-4 border-b-2 border-slate-200 pb-6 text-center sm:mb-8 sm:flex-row sm:items-center sm:gap-6 sm:pb-8 sm:text-left lg:gap-8 dark:border-border-color">
          <img
            :src="user.avatar_url || 'https://i.pravatar.cc/150?img=12'"
            :alt="user.username"
            class="h-24 w-24 rounded-full object-cover sm:h-[110px] sm:w-[110px] lg:h-[120px] lg:w-[120px]"
          />
          <div class="flex-1">
            <h2 class="mb-2 text-xl font-semibold text-slate-800 dark:text-text-primary sm:text-2xl">{{ user.username }}</h2>
            <p class="mb-3 text-sm text-slate-600 dark:text-text-secondary">{{ user.email }}</p>
            <div class="flex flex-wrap gap-2">
              <span class="rounded-md bg-blue-100 px-3 py-1 text-sm font-semibold text-blue-800 dark:bg-blue-900/40 dark:text-blue-300">
                Niveau {{ user.level }}
              </span>
              <span class="rounded-md bg-purple-100 px-3 py-1 text-sm font-semibold text-purple-800 dark:bg-purple-900/40 dark:text-purple-300">
                {{ user.experience_points }} XP
              </span>
            </div>
          </div>
        </div>

        <div v-if="user.bio" class="mb-4">
          <strong class="mb-2 block text-sm text-slate-500 dark:text-text-secondary">À propos</strong>
          <p class="text-slate-700 dark:text-text-primary">{{ user.bio }}</p>
        </div>
      </div>

      <!-- Statistics -->
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div class="rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-border-color dark:bg-bg-tertiary">
          <strong class="mb-2 block text-sm text-slate-500 dark:text-text-secondary">ID</strong>
          <span class="font-medium text-slate-800 dark:text-text-primary">{{ user.id }}</span>
        </div>
        <div class="rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-border-color dark:bg-bg-tertiary">
          <strong class="mb-2 block text-sm text-slate-500 dark:text-text-secondary">Nom d'utilisateur</strong>
          <span class="font-medium text-slate-800 dark:text-text-primary">{{ user.username }}</span>
        </div>
        <div class="rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-border-color dark:bg-bg-tertiary">
          <strong class="mb-2 block text-sm text-slate-500 dark:text-text-secondary">Statut</strong>
          <span class="rounded-md bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300">
            ✓ Actif
          </span>
        </div>
      </div>

      <!-- User's Media -->
      <div v-if="userMedia.length > 0">
        <h3 class="mb-4 text-xl font-semibold text-slate-900 dark:text-text-primary">Mes médias</h3>
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
        <h3 class="mb-4 text-xl font-semibold text-slate-900 dark:text-text-primary">Mes avis</h3>
        <div class="space-y-4">
          <div
            v-for="review in userReviews"
            :key="review.id"
            class="rounded-lg border border-slate-200 bg-white p-4 dark:border-border-color dark:bg-bg-secondary"
          >
            <h4 class="font-semibold text-slate-800 dark:text-text-primary">{{ review.title }}</h4>
            <p class="text-sm text-slate-600 dark:text-text-secondary">{{ review.content }}</p>
            <div class="mt-2 flex gap-2">
              <span class="text-xs text-slate-500 dark:text-text-secondary">{{ new Date(review.created_at).toLocaleDateString() }}</span>
              <span v-if="review.spoiler" class="text-xs text-yellow-600 dark:text-yellow-400">⚠️ Spoiler</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-center gap-4">
        <NuxtLink
          to="/"
          class="inline-block w-full rounded-md bg-accent px-5 py-2.5 text-center text-sm font-semibold text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 active:bg-accent-hover sm:w-auto sm:px-6 sm:py-3 sm:text-base dark:focus:ring-offset-bg-secondary"
        >
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>

    <div v-else-if="!isAuthenticated" class="mt-4 p-4 text-center sm:mt-6 sm:p-6 lg:mt-8 lg:p-8">
      <p class="mb-4 text-slate-600 dark:text-text-secondary">Vous devez être connecté pour voir votre profil.</p>
      <NuxtLink
        to="/users/login"
        class="inline-block rounded-md bg-accent px-5 py-2.5 text-sm font-semibold text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 active:bg-accent-hover sm:px-6 sm:py-3 sm:text-base dark:focus:ring-offset-bg-secondary"
      >
        Se connecter
      </NuxtLink>
    </div>

    <div v-else class="mt-4 p-4 text-center sm:mt-6 sm:p-6 lg:mt-8 lg:p-8">
      Chargement...
    </div>
  </div>
</template>
