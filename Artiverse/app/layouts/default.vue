<script setup lang="ts">
const router = useRouter()
const { isAuthenticated, logout } = useAuth()

const handleLogout = () => {
    logout()
    router.push('/users/login')
}
</script>

<template>

  <div class="flex flex-col min-h-screen bg-gray-50">

    <header class="bg-zinc-900 text-white shadow-md">
      <nav class="container mx-auto flex flex-col gap-3 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:gap-4 sm:px-6 lg:px-8">
        <h1 class="text-xl font-bold tracking-tight sm:text-2xl"><NuxtLink to="/home">Artiverse</NuxtLink></h1>

        <div class="flex items-center gap-x-4 text-sm sm:text-base">
          <NuxtLink to="/" class="transition hover:text-accent-light">Manage</NuxtLink>

          <button v-if="isAuthenticated" @click="handleLogout" class="transition hover:text-accent-light">Se déconnecter</button>
          <template v-else>
            <NuxtLink to="/users/login" class="transition hover:text-accent-light">Se connecter</NuxtLink>
            <NuxtLink
              to="/users/new"
              class="inline-flex items-center rounded-md bg-accent px-3 py-1.5 text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1"
            >
              Créer un compte
            </NuxtLink>
          </template>
          <NuxtLink v-if="isAuthenticated" to="/users/profile" class="transition hover:text-accent-light">Profil</NuxtLink>
        </div>

      </nav>
    </header>
    
    <div class="container mx-auto px-4 py-8 flex-grow flex flex-col md:flex-row gap-8">
      <!-- Main Content -->
      <main class="w-full md:w-3/4">
        <slot />
      </main>
    </div>
    
    <footer class="bg-gray-900 text-white py-6 text-center text-sm mt-auto">
      <p>&copy; {{ new Date().getFullYear() }} Artiverse. All rights reserved.</p>
    </footer>
  </div>
</template>