<script setup lang="ts">
import AppLogo from '~/components/icons/AppLogo.vue';
// @ts-ignore
const { user, isAuthenticated, logout } = useAuth()

const isMenuOpen = ref(false)
const isAdmin = computed(() => user.value?.email?.includes('admin'))

async function handleLogout() {
  isMenuOpen.value = false
  logout()
  await navigateTo('/')
}
</script>

<template>
  <nav class="border-b border-gray-200 bg-white shadow-sm dark:border-border-color dark:bg-bg-secondary">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">

        <!-- Logo + main nav -->
        <div class="flex items-center gap-6">
          <div class="flex-shrink-0">
            <AppLogo showText size="medium" />
          </div>

          <div class="hidden sm:flex sm:items-center sm:gap-1">
            <NuxtLink to="/"
              class="inline-flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-500 transition-colors hover:bg-gray-100 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent">
              Accueil
            </NuxtLink>
            <NuxtLink v-if="isAuthenticated" to="/search"
              class="inline-flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-500 transition-colors hover:bg-gray-100 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent">
              Catalogue
            </NuxtLink>
            <NuxtLink v-if="isAuthenticated" to="/mylists"
              class="inline-flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-500 transition-colors hover:bg-gray-100 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent">
              Mes listes
            </NuxtLink>
            <NuxtLink v-if="isAuthenticated" to="/badges"
              class="inline-flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-500 transition-colors hover:bg-gray-100 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent">
              Badges
            </NuxtLink>
            <NuxtLink v-if="isAuthenticated" to="/feed"
              class="inline-flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-500 transition-colors hover:bg-gray-100 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent">
              Fil d'actualité
            </NuxtLink>
          </div>
        </div>

        <!-- Right section -->
        <div class="hidden sm:flex sm:items-center sm:gap-3">
          <ThemeToggle />

          <!-- Authenticated -->
          <div v-if="isAuthenticated && user" class="flex items-center gap-3">
            <NuxtLink :to="`/users/${user.id}`" class="flex items-center gap-2.5 rounded-xl px-3 py-1.5 transition-colors hover:bg-bg-tertiary">
              <img v-if="user.avatar_url" :src="user.avatar_url" :alt="user.username"
                class="h-8 w-8 flex-shrink-0 rounded-full object-cover" />
              <div v-else class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-accent to-accent-series text-sm font-bold text-white">
                {{ user.username[0]?.toUpperCase() }}
              </div>
              <span class="text-sm font-semibold text-gray-700 dark:text-text-primary">{{ user.username }}</span>
            </NuxtLink>

            <button @click="handleLogout"
              class="rounded-md border border-red-300 px-3 py-1.5 text-sm font-medium text-red-600 transition-all hover:bg-red-50 focus:outline-none dark:border-red-800 dark:text-red-400 dark:hover:bg-red-900/20">
              Déconnexion
            </button>
          </div>

          <!-- Not authenticated -->
          <div v-else class="flex items-center gap-3">
            <NuxtLink to="/users/login"
              class="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 transition-all hover:bg-gray-50 dark:border-border-color dark:text-text-secondary dark:hover:bg-bg-tertiary">
              Connexion
            </NuxtLink>
            <NuxtLink to="/users/new"
              class="rounded-md bg-accent px-3 py-1.5 text-sm font-medium text-white transition-all hover:bg-accent-hover">
              Inscription
            </NuxtLink>
          </div>
        </div>

        <!-- Mobile controls -->
        <div class="flex items-center gap-2 sm:hidden">
          <ThemeToggle />
          <button @click="isMenuOpen = !isMenuOpen" type="button"
            class="inline-flex items-center justify-center rounded-md p-2 text-gray-400 transition-all hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-accent dark:text-text-secondary dark:hover:bg-bg-tertiary">
            <span class="sr-only">Ouvrir le menu</span>
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path v-if="!isMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-if="isMenuOpen" class="border-t border-gray-200 dark:border-border-color sm:hidden">
      <div class="space-y-1 px-4 py-3">
        <NuxtLink to="/" @click="isMenuOpen = false"
          class="block rounded-lg px-3 py-2.5 text-base font-medium text-gray-600 transition-colors hover:bg-gray-100 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent">
          Accueil
        </NuxtLink>
        <template v-if="isAuthenticated">
          <NuxtLink to="/search" @click="isMenuOpen = false"
            class="block rounded-lg px-3 py-2.5 text-base font-medium text-gray-600 transition-colors hover:bg-gray-100 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent">
            Catalogue
          </NuxtLink>
          <NuxtLink to="/mylists" @click="isMenuOpen = false"
            class="block rounded-lg px-3 py-2.5 text-base font-medium text-gray-600 transition-colors hover:bg-gray-100 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent">
            Mes listes
          </NuxtLink>
          <NuxtLink to="/badges" @click="isMenuOpen = false"
            class="block rounded-lg px-3 py-2.5 text-base font-medium text-gray-600 transition-colors hover:bg-gray-100 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent">
            Badges
          </NuxtLink>
          <NuxtLink to="/feed" @click="isMenuOpen = false"
            class="block rounded-lg px-3 py-2.5 text-base font-medium text-gray-600 transition-colors hover:bg-gray-100 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent">
            Fil d'actualité
          </NuxtLink>
        </template>
      </div>

      <!-- Mobile user section -->
      <div v-if="isAuthenticated && user" class="border-t border-gray-200 px-4 py-3 dark:border-border-color">
        <div class="mb-3 flex items-center gap-3">
          <img v-if="user.avatar_url" :src="user.avatar_url" :alt="user.username"
            class="h-10 w-10 flex-shrink-0 rounded-full object-cover" />
          <div v-else class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-accent to-accent-series text-sm font-bold text-white">
            {{ user.username[0]?.toUpperCase() }}
          </div>
          <div>
            <div class="font-semibold text-gray-800 dark:text-text-primary">{{ user.username }}</div>
            <div class="text-sm text-gray-500 dark:text-text-secondary">Niveau {{ user.level }}</div>
          </div>
        </div>
        <div class="space-y-1">
          <NuxtLink :to="`/users/${user.id}`" @click="isMenuOpen = false"
            class="block rounded-lg px-3 py-2 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-100 dark:text-text-secondary dark:hover:bg-bg-tertiary">
            Mon profil
          </NuxtLink>
          <button @click="handleLogout"
            class="block w-full rounded-lg px-3 py-2 text-left text-sm font-medium text-red-500 transition-colors hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20">
            Déconnexion
          </button>
        </div>
      </div>

      <div v-else class="border-t border-gray-200 px-4 py-3 dark:border-border-color">
        <div class="space-y-2">
          <NuxtLink to="/users/login" @click="isMenuOpen = false"
            class="block rounded-md border border-gray-300 px-4 py-2 text-center text-base font-medium text-gray-700 hover:bg-gray-50 dark:border-border-color dark:text-text-secondary dark:hover:bg-bg-tertiary">
            Connexion
          </NuxtLink>
          <NuxtLink to="/users/new" @click="isMenuOpen = false"
            class="block rounded-md bg-accent px-4 py-2 text-center text-base font-medium text-white hover:bg-accent-hover">
            Inscription
          </NuxtLink>
        </div>
      </div>
    </div>
  </nav>
</template>
