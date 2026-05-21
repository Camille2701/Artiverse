<script setup lang="ts">
// @ts-ignore
const { user, isAuthenticated, logout } = useAuth()
// @ts-ignore
const { isDark } = useTheme()
const isMenuOpen = ref(false)

async function handleLogout() {
  logout()
  await navigateTo('/')
}
</script>

<template>
  <nav class="border-b border-gray-200 bg-white shadow-sm dark:border-border-color dark:bg-bg-secondary">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 justify-between">
        <!-- Logo and main navigation -->
        <div class="flex">
          <div class="flex flex-shrink-0 items-center">
            <NuxtLink to="/" class="text-2xl font-bold text-accent">
              🎬 Artiverse
            </NuxtLink>
          </div>

          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <NuxtLink
              to="/"
              class="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-500 transition-colors hover:border-accent hover:text-accent"
            >
              Accueil
            </NuxtLink>

            <NuxtLink
              v-if="isAuthenticated"
              :to="`/users/${user?.id}`"
              class="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-500 transition-colors hover:border-accent hover:text-accent"
            >
              Mon profil
            </NuxtLink>

            <NuxtLink
              v-if="isAuthenticated"
              :to="`/users/${user?.id}/lists`"
              class="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-500 transition-colors hover:border-accent hover:text-accent"
            >
              Mes listes
            </NuxtLink>
          </div>
        </div>

        <!-- Auth buttons and theme toggle -->
        <div class="hidden sm:ml-6 sm:flex sm:items-center sm:gap-4">
          <!-- Theme toggle -->
          <ThemeToggle />

          <div v-if="isAuthenticated && user" class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <img
                v-if="user.avatar_url"
                :src="user.avatar_url"
                :alt="user.username"
                class="h-8 w-8 rounded-full object-cover"
              />
              <span class="text-sm font-medium text-gray-700 dark:text-text-primary">{{ user.username }}</span>
              <span class="rounded-full bg-blue-100 px-2 py-0.5 text-xs font-semibold text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                Niv. {{ user.level }}
              </span>
            </div>
            <button
              @click="handleLogout"
              class="rounded-md border border-red-300 px-3 py-1.5 text-sm font-medium text-red-600 transition-all duration-200 ease-out hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1 dark:border-red-800 dark:text-red-400 dark:hover:bg-red-900/20 dark:focus:ring-red-600 dark:focus:ring-offset-bg-secondary"
            >
              Déconnexion
            </button>
          </div>

          <div v-else class="flex items-center gap-3">
            <NuxtLink
              to="/users/login"
              class="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 transition-all duration-200 ease-out hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-1 dark:border-border-color dark:text-text-secondary dark:hover:bg-bg-tertiary dark:focus:ring-gray-600 dark:focus:ring-offset-bg-secondary"
            >
              Connexion
            </NuxtLink>
            <NuxtLink
              to="/users/new"
              class="rounded-md bg-accent px-3 py-1.5 text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 dark:focus:ring-offset-bg-secondary"
            >
              Inscription
            </NuxtLink>
          </div>
        </div>

        <!-- Mobile menu button -->
        <div class="flex items-center gap-2 sm:hidden">
          <!-- Theme toggle for mobile -->
          <ThemeToggle />

          <button
            @click="isMenuOpen = !isMenuOpen"
            type="button"
            class="inline-flex items-center justify-center rounded-md p-2 text-gray-400 transition-all duration-200 ease-out hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-text-primary dark:focus:ring-accent"
            aria-controls="mobile-menu"
            aria-expanded="false"
          >
            <span class="sr-only">Ouvrir le menu principal</span>
            <svg
              class="h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path v-if="!isMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-if="isMenuOpen" class="sm:hidden" id="mobile-menu">
      <div class="space-y-1 pt-2 pb-3">
        <NuxtLink
          to="/"
          class="block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 transition-all duration-200 ease-out hover:border-accent hover:bg-gray-50 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent"
          @click="isMenuOpen = false"
        >
          Accueil
        </NuxtLink>

        <NuxtLink
          v-if="isAuthenticated"
          :to="`/users/${user?.id}`"
          class="block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 transition-all duration-200 ease-out hover:border-accent hover:bg-gray-50 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent"
          @click="isMenuOpen = false"
        >
          Mon profil
        </NuxtLink>

        <NuxtLink
          v-if="isAuthenticated"
          :to="`/users/${user?.id}/lists`"
          class="block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 transition-all duration-200 ease-out hover:border-accent hover:bg-gray-50 hover:text-accent dark:text-text-secondary dark:hover:bg-bg-tertiary dark:hover:text-accent"
          @click="isMenuOpen = false"
        >
          Mes listes
        </NuxtLink>
      </div>

      <div class="border-t border-gray-200 pt-4 pb-3 dark:border-border-color">
        <div v-if="isAuthenticated && user" class="space-y-3">
          <div class="flex items-center px-4">
            <div class="flex-shrink-0">
              <img
                v-if="user.avatar_url"
                :src="user.avatar_url"
                :alt="user.username"
                class="h-10 w-10 rounded-full object-cover"
              />
              <div v-else class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center dark:bg-bg-tertiary dark:text-text-primary">
                <span class="text-gray-600 dark:text-text-primary">{{ user.username[0]?.toUpperCase() }}</span>
              </div>
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800 dark:text-text-primary">{{ user.username }}</div>
              <div class="text-sm font-medium text-gray-500 dark:text-text-secondary">{{ user.email }}</div>
            </div>
          </div>
          <div class="mt-3 space-y-1">
            <button
              @click="handleLogout(); isMenuOpen = false"
              class="block w-full rounded-md border border-red-300 bg-transparent px-4 py-2 text-left text-base font-medium text-red-600 transition-all duration-200 ease-out hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 dark:border-red-800 dark:text-red-400 dark:hover:bg-red-900/20 dark:focus:ring-red-600"
            >
              Déconnexion
            </button>
          </div>
        </div>

        <div v-else class="mt-3 space-y-1">
          <NuxtLink
            to="/users/login"
            class="block rounded-md border border-gray-300 bg-transparent px-4 py-2 text-base font-medium text-gray-700 transition-all duration-200 ease-out hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 dark:border-border-color dark:text-text-secondary dark:hover:bg-bg-tertiary dark:focus:ring-gray-600"
            @click="isMenuOpen = false"
          >
            Connexion
          </NuxtLink>
          <NuxtLink
            to="/users/new"
            class="block rounded-md bg-accent px-4 py-2 text-base font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent"
            @click="isMenuOpen = false"
          >
            Inscription
          </NuxtLink>
        </div>
      </div>
    </div>
  </nav>
</template>