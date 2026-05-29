<script setup lang="ts">
import UIIcon from '~/components/icons/UIIcon.vue';

const router = useRouter()
const { isAuthenticated, logout } = useAuth()
const { isDark } = useTheme()

const handleLogout = () => {
    logout()
    router.push('/users/login')
}

// Enable dark mode by default
onMounted(() => {
  document.documentElement.classList.add('dark')
})

const logoSrc = computed(() => {
  return isDark.value
    ? '/logos/small_white_bg.png'
    : '/logos/small.png';
});
</script>

<template>
  <div class="flex flex-col min-h-screen bg-bg-primary noise">

    <header class="glass border-b border-border-color/50 sticky top-0 z-50">
      <nav class="container mx-auto flex flex-col gap-4 px-4 py-3 sm:flex-row sm:items-center sm:justify-between sm:gap-6 sm:px-6 lg:px-8">
        <div class="flex items-center gap-3">
          <NuxtLink to="/" class="flex items-center gap-3 group">
            <div class="relative h-11 w-11">
                <img
                  :src="logoSrc"
                  alt="Artiverse Logo"
                  class="h-8 w-8 object-contain"
                />
              </div>
            <h1 class="text-2xl font-display font-bold tracking-tight text-text-primary group-hover:gradient-text transition-all duration-300">
              Artiverse
            </h1>
          </NuxtLink>
        </div>

        <div class="flex items-center gap-2 sm:gap-6">
          <div class="group">
            <NuxtLink to="/home" class="nav-link text-sm px-3 py-2 rounded-lg hover:bg-bg-secondary/50 transition-all duration-300">
              Catalogue
            </NuxtLink>
          </div>

          <template v-if="isAuthenticated">
            <div class="group">
              <NuxtLink to="/users/profile" class="nav-link text-sm px-3 py-2 rounded-lg hover:bg-bg-secondary/50 transition-all duration-300 flex items-center gap-2">
                <UIIcon name="user" size="small" />
                <span class="hidden sm:inline">Profil</span>
              </NuxtLink>
            </div>
            <div class="group">
              <button
                @click="handleLogout"
                class="nav-link text-sm px-3 py-2 rounded-lg hover:bg-bg-secondary/50 transition-all duration-300 flex items-center gap-2"
              >
                <UIIcon name="close" size="small" />
                <span class="hidden sm:inline">Se déconnecter</span>
              </button>
            </div>
          </template>
          <template v-else>
            <div class="group">
              <NuxtLink to="/users/login" class="nav-link text-sm px-3 py-2 rounded-lg hover:bg-bg-secondary/50 transition-all duration-300">
                Se connecter
              </NuxtLink>
            </div>
            <NuxtLink
              to="/users/new"
              class="btn-primary text-sm px-5 py-2.5"
            >
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