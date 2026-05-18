<script setup lang="ts">
import type { User } from '../../../types/user'

useHead({
  title: "Artiverse",
  meta: [
    { name: "Page de consultation d'un utilisateur", content: "Consultation d'un utilisateur"}
  ]
})

const route = useRoute()
const userId = route.params.id as string

const user = ref<User | null>(null)
const error = ref(false)

onMounted(() => {
  const stored = sessionStorage.getItem(`user_${userId}`)
  if (stored) {
    user.value = JSON.parse(stored)
    return
  }

  $fetch<User[]>('/api/users')
    .then(users => {
      user.value = users.find(u => u.id === Number(userId)) || null
      if (!user.value) {
        error.value = true
      }
    })
    .catch(() => {
      error.value = true
    })
})
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-3xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">
    <h1 class="text-2xl font-semibold text-slate-900 sm:text-3xl">Mon profil</h1>

    <div v-if="error" class="mt-4 p-4 text-center sm:mt-6 sm:p-6 lg:mt-8 lg:p-8">
      <h2 class="mb-4 text-xl font-semibold text-red-500 sm:text-2xl">Utilisateur introuvable</h2>
      <NuxtLink
        to="/"
        class="inline-block rounded-md bg-slate-600 px-5 py-2.5 text-sm font-semibold text-white transition-all duration-200 ease-out hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-1 active:bg-slate-800 sm:px-6 sm:py-3 sm:text-base"
      >
        Retour à l'accueil
      </NuxtLink>
    </div>

    <div v-else-if="user" class="mt-4 rounded-xl bg-white p-4 shadow-md sm:mt-6 sm:p-6 lg:mt-8 lg:p-8">
      <div class="mb-6 flex flex-col items-center gap-4 border-b-2 border-slate-200 pb-6 text-center sm:mb-8 sm:flex-row sm:items-center sm:gap-6 sm:pb-8 sm:text-left lg:gap-8">
        <img :src="user.avatar" :alt="user.name" class="h-24 w-24 rounded-full object-cover sm:h-[110px] sm:w-[110px] lg:h-[120px] lg:w-[120px]" />
        <div>
          <h2 class="mb-2 text-xl font-semibold text-slate-800 sm:text-2xl">{{ user.name }}</h2>
          <span
            class="rounded-md px-4 py-2 text-sm font-semibold"
            :class="user.isActive ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'"
          >
            {{ user.isActive ? '✓ Actif' : '○ Inactif' }}
          </span>
        </div>
      </div>

      <div class="mb-6 grid grid-cols-1 gap-3 sm:mb-8 sm:gap-4 lg:grid-cols-2">
        <div class="rounded-lg border border-slate-200 bg-slate-50 p-4">
          <strong class="mb-2 block text-sm text-slate-500">Email</strong>
          <span class="font-medium text-slate-800">{{ user.email }}</span>
        </div>
        <div class="rounded-lg border border-slate-200 bg-slate-50 p-4">
          <strong class="mb-2 block text-sm text-slate-500">Âge</strong>
          <span class="font-medium text-slate-800">{{ user.age }} ans</span>
        </div>
        <div class="rounded-lg border border-slate-200 bg-slate-50 p-4">
          <strong class="mb-2 block text-sm text-slate-500">ID</strong>
          <span class="font-medium text-slate-800">#{{ user.id }}</span>
        </div>
        <div class="rounded-lg border border-slate-200 bg-slate-50 p-4">
          <strong class="mb-2 block text-sm text-slate-500">Rôle</strong>
          <span class="font-medium text-slate-800">{{ user.role }}</span>
        </div>
      </div>

      <div class="flex justify-center gap-4">
        <NuxtLink
          to="/"
          class="inline-block w-full rounded-md bg-accent px-5 py-2.5 text-center text-sm font-semibold text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 active:bg-accent-hover sm:w-auto sm:px-6 sm:py-3 sm:text-base"
        >
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>

    <div v-else class="mt-4 p-4 text-center sm:mt-6 sm:p-6 lg:mt-8 lg:p-8">
      Chargement...
    </div>
  </div>
</template>
