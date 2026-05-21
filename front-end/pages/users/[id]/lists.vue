<script setup lang="ts">
import type { User } from '../../../types/user'

useHead({
  title: "Artiverse - Mes listes",
  meta: [
    { name: "Page des listes de l'utilisateur", content: "Listes de l'utilisateur"}
  ]
})

const route = useRoute()
const userId = route.params.id as string
const { user: currentUser, isAuthenticated, logout } = useAuth()
const { fetchWithAuth, getErrorMessage, isLoading, error } = useApi()

const user = ref<User | null>(null)
const userLists = ref<any[]>([])
const newListName = ref('')
const newListVisibility = ref('private')
const isCreating = ref(false)
const showCreateForm = ref(false)
const createError = ref('')

async function fetchUserLists() {
  try {
    if (isAuthenticated.value && currentUser.value) {
      user.value = currentUser.value

      const response = await fetchWithAuth(`/api/v1/users/${user.value.id}/lists`)
      userLists.value = response?.lists || []
    }
  } catch (err: any) {
    error.value = err
  }
}

async function createList() {
  if (!newListName.value.trim()) {
    createError.value = 'Le nom de la liste est requis.'
    return
  }

  isCreating.value = true
  createError.value = ''

  try {
    const newList = await fetchWithAuth('/api/v1/lists', {
      method: 'POST',
      body: {
        name: newListName.value,
        visibility: newListVisibility.value
      }
    })

    userLists.value.push(newList)
    newListName.value = ''
    newListVisibility.value = 'private'
    showCreateForm.value = false
  } catch (err: any) {
    createError.value = getErrorMessage(err)
  } finally {
    isCreating.value = false
  }
}

async function deleteList(listId: string) {
  if (!confirm('Êtes-vous sûr de vouloir supprimer cette liste ?')) {
    return
  }

  try {
    await fetchWithAuth(`/api/v1/lists/${listId}`, {
      method: 'DELETE'
    })
    userLists.value = userLists.value.filter(list => list.id !== listId)
  } catch (err: any) {
    alert(getErrorMessage(err))
  }
}

async function handleLogout() {
  logout()
  await navigateTo('/')
}

onMounted(fetchUserLists)
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-5xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-slate-900 sm:text-3xl">Mes listes</h1>
      <div class="flex gap-2">
        <button
          v-if="isAuthenticated"
          @click="handleLogout"
          class="rounded-md border border-red-300 px-4 py-2 text-sm font-medium text-red-600 transition-all duration-200 ease-out hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1 sm:text-base"
        >
          Déconnexion
        </button>
        <NuxtLink
          to="/"
          class="rounded-md bg-slate-600 px-4 py-2 text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-1 sm:text-base"
        >
          Accueil
        </NuxtLink>
      </div>
    </div>

    <div v-if="!isAuthenticated" class="rounded-md bg-blue-50 p-6">
      <div class="flex items-start gap-4">
        <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-blue-100">
          <span class="text-blue-600">ℹ️</span>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-medium text-blue-800">Connexion requise</h3>
          <p class="mt-2 text-sm text-blue-700">Vous devez être connecté pour voir vos listes.</p>
          <NuxtLink
            to="/users/login"
            class="mt-4 inline-flex items-center rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1"
          >
            Se connecter
          </NuxtLink>
        </div>
      </div>
    </div>

    <div v-else-if="isLoading" class="flex items-center justify-center py-20">
      <div class="h-12 w-12 animate-spin rounded-full border-b-2 border-accent"></div>
      <p class="ml-3 text-gray-600">Chargement de vos listes...</p>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-6">
      <h3 class="text-lg font-medium text-red-800">Erreur de chargement</h3>
      <p class="mt-2 text-sm text-red-700">{{ getErrorMessage(error) }}</p>
    </div>

    <div v-else class="space-y-6">
      <!-- Create List Form -->
      <div v-if="showCreateForm" class="rounded-xl bg-white p-6 shadow-md">
        <h3 class="mb-4 text-lg font-semibold text-gray-900">Créer une nouvelle liste</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Nom de la liste</label>
            <input
              v-model="newListName"
              type="text"
              placeholder="Ma liste préférée"
              class="mt-1 block w-full rounded-md border px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Visibilité</label>
            <select
              v-model="newListVisibility"
              class="mt-1 block w-full rounded-md border px-3 py-2 text-sm"
            >
              <option value="private">Privée</option>
              <option value="friends">Amis</option>
              <option value="public">Publique</option>
            </select>
          </div>
          <div v-if="createError" class="rounded-md bg-red-50 p-3">
            <p class="text-sm text-red-800">{{ createError }}</p>
          </div>
          <div class="flex gap-2">
            <button
              @click="createList"
              :disabled="isCreating"
              class="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 disabled:opacity-50"
            >
              {{ isCreating ? 'Création...' : 'Créer' }}
            </button>
            <button
              @click="showCreateForm = false"
              class="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition-all duration-200 ease-out hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-1"
            >
              Annuler
            </button>
          </div>
        </div>
      </div>

      <!-- Lists Grid -->
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <button
          v-if="!showCreateForm"
          @click="showCreateForm = true"
          class="flex h-full flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 p-6 transition-all duration-200 ease-out hover:border-accent hover:bg-gray-100"
        >
          <span class="text-4xl">+</span>
          <span class="mt-2 text-sm font-medium text-gray-600">Créer une liste</span>
        </button>

        <div
          v-for="list in userLists"
          :key="list.id"
          class="rounded-xl bg-white p-6 shadow-md transition-all duration-200 ease-out hover:shadow-lg"
        >
          <div class="mb-4 flex items-start justify-between">
            <h3 class="text-lg font-semibold text-gray-900">{{ list.name }}</h3>
            <span
              class="rounded-full px-2 py-1 text-xs font-medium"
              :class="{
                'bg-green-100 text-green-800': list.visibility === 'public',
                'bg-blue-100 text-blue-800': list.visibility === 'friends',
                'bg-gray-100 text-gray-800': list.visibility === 'private'
              }"
            >
              {{ list.visibility === 'public' ? 'Publique' : list.visibility === 'friends' ? 'Amis' : 'Privée' }}
            </span>
          </div>

          <div class="mb-4 flex items-center justify-between text-sm text-gray-500">
            <span>{{ list.items?.length || 0 }} média(s)</span>
            <span>{{ new Date(list.created_at).toLocaleDateString('fr-FR') }}</span>
          </div>

          <div class="flex gap-2">
            <NuxtLink
              :to="`/users/${user?.id}/lists/${list.id}`"
              class="flex-1 rounded-md bg-accent px-3 py-2 text-center text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1"
            >
              Voir
            </NuxtLink>
            <button
              @click="deleteList(list.id)"
              class="rounded-md border border-red-300 px-3 py-2 text-sm font-medium text-red-600 transition-all duration-200 ease-out hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1"
            >
              Supprimer
            </button>
          </div>
        </div>
      </div>

      <div v-if="userLists.length === 0 && !showCreateForm" class="text-center py-12">
        <p class="text-gray-500">Vous n'avez pas encore de listes. Créez votre première liste !</p>
      </div>
    </div>
  </div>
</template>