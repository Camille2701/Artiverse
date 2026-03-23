<script setup lang="ts">
const router = useRouter()
const route = useRoute()
const { isAuthenticated, logout } = useAuth()

const handleLogout = () => {
    logout()
    router.push('/users/login')
}
</script>

<template>

  <div class="flex flex-col min-h-screen bg-gray-50">

    <header class="bg-gray-900 text-white shadow-md">
      <nav class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold tracking-tight"><NuxtLink to="/home">Artiverse</NuxtLink></h1>
        <div class="space-x-4">
          <NuxtLink to="/" class="hover:text-indigo-200 transition">Manage</NuxtLink>

          <button v-if="isAuthenticated" @click="handleLogout" class="hover:text-indigo-200 transition">Se déconnecter</button>
          <NuxtLink v-else to="/users/login" class="hover:text-indigo-200 transition">Se connecter</NuxtLink>
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