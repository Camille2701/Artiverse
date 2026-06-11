<script setup lang="ts">
import UIIcon from '~/components/icons/UIIcon.vue'
import ThemeToggle from '~/components/ThemeToggle.vue'

const router = useRouter()
const { isAuthenticated, logout, user } = useAuth()
const { isDark } = useTheme()

const handleLogout = () => {
  logout()
  router.push('/users/login')
}

const logoSrc = computed(() => {
  return isDark.value
    ? '/logos/small_white_bg.png'
    : '/logos/small.png'
})

const profilePath = computed(() =>
  user.value?.id ? `/users/${user.value.id}` : '/users/profile'
)

const showProfileMenu = ref(false)
</script>

<template>
  <div class="flex flex-col min-h-screen bg-bg-primary noise">

    <header class="glass border-b border-border-color/50 sticky top-0 z-50">
      <nav class="container mx-auto flex flex-col gap-4 px-4 py-3 sm:flex-row sm:items-center sm:justify-between sm:gap-6 sm:px-6 lg:px-8">
        <div class="flex items-center gap-3">
          <NuxtLink to="/" class="flex items-center gap-2.5 group">
            <div class="flex h-10 w-10 shrink-0 items-center justify-center">
              <img
                :src="logoSrc"
                alt="Artiverse Logo"
                class="h-9 w-9 object-contain"
              />
            </div>
            <span class="text-2xl font-display font-bold leading-none tracking-tight text-text-primary group-hover:gradient-text transition-all duration-300">
              Artiverse
            </span>
          </NuxtLink>
        </div>

        <div class="flex flex-wrap items-center gap-1 sm:gap-2">
          <NuxtLink to="/home" class="nav-link text-sm px-3 py-2 rounded-lg hover:bg-bg-secondary/50 transition-all duration-300">
            Catalogue
          </NuxtLink>
          <NuxtLink to="/search" class="nav-link text-sm px-3 py-2 rounded-lg hover:bg-bg-secondary/50 transition-all duration-300">
            Recherche
          </NuxtLink>
          <template v-if="isAuthenticated">
            <NuxtLink to="/mylists" class="nav-link text-sm px-3 py-2 rounded-lg hover:bg-bg-secondary/50 transition-all duration-300">
              Mes listes
            </NuxtLink>
            <NuxtLink to="/statistics" class="nav-link text-sm px-3 py-2 rounded-lg hover:bg-bg-secondary/50 transition-all duration-300 hidden md:inline-flex">
              Statistiques
            </NuxtLink>
          </template>

          <ThemeToggle />

          <template v-if="isAuthenticated">
            <!-- Profile Dropdown -->
            <div class="relative" @click.outside="showProfileMenu = false">
              <button
                @click.stop="showProfileMenu = !showProfileMenu"
                class="nav-link text-sm px-3 py-2 rounded-lg hover:bg-bg-secondary/50 transition-all duration-300 flex items-center gap-2"
                aria-label="Menu profil"
                aria-expanded="showProfileMenu"
              >
                <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-bg-tertiary">
                  <UIIcon name="user" size="small" />
                </span>
                <span class="hidden sm:inline">{{ user?.username || 'Profil' }}</span>
                <UIIcon name="chevron-down" size="small" class="hidden sm:inline" />
              </button>

              <!-- Dropdown Menu -->
              <div
                v-if="showProfileMenu"
                class="absolute right-0 mt-2 w-48 rounded-lg glass border border-border-color shadow-xl z-50"
                @click.stop="showProfileMenu = false"
              >
                <div class="py-1">
                  <NuxtLink
                    :to="profilePath"
                    class="block px-4 py-2 text-sm text-text-primary hover:bg-bg-secondary/50 transition-colors"
                  >
                    <span class="flex items-center gap-2">
                      <UIIcon name="user" size="small" />
                      Mon profil
                    </span>
                  </NuxtLink>
                  <div class="border-t border-border-color my-1"></div>
                  <button
                    @click.stop="handleLogout(); showProfileMenu = false"
                    class="block w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-red-500/10 transition-colors"
                  >
                    <span class="flex items-center gap-2">
                      <UIIcon name="close" size="small" />
                      Déconnexion
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </template>
          <template v-else>
            <NuxtLink to="/users/login" class="nav-link text-sm px-3 py-2 rounded-lg hover:bg-bg-secondary/50 transition-all duration-300">
              Se connecter
            </NuxtLink>
            <NuxtLink to="/users/new" class="btn-primary text-sm px-5 py-2.5">
              Créer un compte
            </NuxtLink>
          </template>
        </div>
      </nav>
    </header>

    <div class="container mx-auto px-4 py-8 flex-grow">
      <!-- Main Content -->
      <main class="max-w-7xl mx-auto">
        <slot />
      </main>
    </div>

    <footer class="glass border-t border-border-color/50 mt-auto">
      <div class="container mx-auto px-4 py-8">
        <div class="flex flex-col md:flex-row justify-between items-center gap-6">
          <div class="flex items-center gap-3">
            <div class="h-8 w-8 rounded-lg bg-gradient-to-br from-accent-movie via-accent-series to-accent-game flex items-center justify-center">
              <img
                :src="logoSrc"
                alt="Artiverse Logo"
                class="h-6 w-6 object-contain"
              />
            </div>
            <p class="text-text-secondary text-sm font-body">
              &copy; {{ new Date().getFullYear() }} Artiverse. Tous droits réservés.
            </p>
          </div>
          <div class="flex gap-6">
            <a href="#" class="text-text-secondary hover:text-text-primary transition-colors text-sm font-body hover:underline underline-offset-4">
              À propos
            </a>
            <a href="#" class="text-text-secondary hover:text-text-primary transition-colors text-sm font-body hover:underline underline-offset-4">
              Confidentialité
            </a>
            <a href="#" class="text-text-secondary hover:text-text-primary transition-colors text-sm font-body hover:underline underline-offset-4">
              Conditions
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>