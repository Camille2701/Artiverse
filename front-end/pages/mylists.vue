<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useLists } from '~/composables/useLists'
import type { MediaList } from '~/types/list'

const { getAllLists, createList, updateList, deleteList } = useLists()

const lists = ref<MediaList[]>([])
const isLoading = ref(false)
const showCreateForm = ref(false)
const editingList = ref<MediaList | null>(null)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

const newList = ref({
  name: '',
  visibility: 'private'
})

onMounted(async () => {
  await loadLists()
})

async function loadLists() {
  try {
    isLoading.value = true
    lists.value = await getAllLists()
  } catch (error: any) {
    message.value = 'Erreur lors du chargement des listes'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleCreateList() {
  try {
    isLoading.value = true
    await createList(newList.value)
    message.value = 'Liste créée avec succès !'
    messageType.value = 'success'
    showCreateForm.value = false
    newList.value = { name: '', visibility: 'private' }
    await loadLists()
  } catch (error: any) {
    message.value = error.message || 'Erreur lors de la création de la liste'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleUpdateList() {
  if (!editingList.value) return
  try {
    isLoading.value = true
    await updateList(editingList.value.id, {
      name: editingList.value.name,
      visibility: editingList.value.visibility
    })
    message.value = 'Liste mise à jour avec succès !'
    messageType.value = 'success'
    editingList.value = null
    await loadLists()
  } catch (error: any) {
    message.value = error.message || 'Erreur lors de la mise à jour de la liste'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleDeleteList(listId: string) {
  if (!confirm('Êtes-vous sûr de vouloir supprimer cette liste ?')) return
  try {
    isLoading.value = true
    await deleteList(listId)
    message.value = 'Liste supprimée avec succès !'
    messageType.value = 'success'
    await loadLists()
  } catch (error: any) {
    message.value = error.message || 'Erreur lors de la suppression de la liste'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

const visibilityConfig = {
  private: {
    label: 'Privée',
    color: 'bg-gray-100 text-gray-800 dark:bg-gray-900/50 dark:text-gray-400'
  },
  friends: {
    label: 'Amis',
    color: 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-400'
  },
  public: {
    label: 'Publique',
    color: 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-400'
  }
}
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-6xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl sm:text-3xl font-display font-bold text-text-primary">Mes listes</h1>
      <button
        @click="showCreateForm = !showCreateForm"
        class="btn-primary px-4 py-2 rounded-lg"
      >
        {{ showCreateForm ? 'Annuler' : 'Créer une liste' }}
      </button>
    </div>

    <!-- Alert Message -->
    <div
      v-if="message"
      :class="[
        'p-4 rounded-lg mb-6',
        messageType === 'success'
          ? 'bg-emerald-500/20 text-emerald-200 border border-emerald-500/30'
          : 'bg-red-500/20 text-red-200 border border-red-500/30'
      ]"
    >
      {{ message }}
    </div>

    <!-- Create Form -->
    <div v-if="showCreateForm" class="glass rounded-xl p-6 mb-6 border border-border-color">
      <h2 class="text-xl font-semibold mb-4 text-text-primary font-display">Créer une nouvelle liste</h2>
      <form @submit.prevent="handleCreateList" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2 text-text-primary font-display">Nom de la liste</label>
          <input
            v-model="newList.name"
            type="text"
            required
            class="input-field"
            placeholder="Ma liste de films préférés"
          />
        </div>
        <div>
          <label class="block text-sm font-medium mb-2 text-text-primary font-display">Visibilité</label>
          <select
            v-model="newList.visibility"
            class="input-field"
          >
            <option value="private">Privée</option>
            <option value="friends">Amis uniquement</option>
            <option value="public">Publique</option>
          </select>
        </div>
        <button
          type="submit"
          :disabled="isLoading"
          class="btn-primary"
        >
          {{ isLoading ? 'Création...' : 'Créer la liste' }}
        </button>
      </form>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && lists.length === 0" class="flex flex-col items-center justify-center py-20">
      <div class="spinner !h-12 !w-12 !border-4"></div>
      <p class="mt-4 text-text-secondary font-body">Chargement des listes...</p>
    </div>

    <!-- Lists Grid -->
    <div v-else-if="lists.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="list in lists"
        :key="list.id"
        class="glass rounded-xl p-6 border border-border-color hover:border-border-color-light transition-all duration-300"
      >
        <div class="flex justify-between items-start mb-4">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-text-primary font-display">{{ list.name }}</h3>
            <span
              :class="['px-2 py-1 rounded text-xs mt-2 inline-block font-medium', visibilityConfig[list.visibility]?.color]"
            >
              {{ visibilityConfig[list.visibility]?.label || list.visibility }}
            </span>
          </div>
          <div class="flex space-x-2">
            <button
              @click="editingList = list"
              class="text-accent hover:text-accent-hover transition-colors text-sm font-medium"
            >
              Modifier
            </button>
            <button
              @click="handleDeleteList(list.id)"
              class="text-red-400 hover:text-red-300 transition-colors text-sm font-medium"
            >
              Supprimer
            </button>
          </div>
        </div>
        <div class="text-sm text-text-secondary font-body">
          {{ list.items?.length || 0 }} médias
        </div>
        <NuxtLink
          :to="`/lists/${list.id}`"
          class="mt-4 inline-block text-accent hover:text-accent-hover text-sm font-medium transition-colors"
        >
          Voir les détails →
        </NuxtLink>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingList" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="glass rounded-xl p-6 max-w-md w-full border border-border-color">
        <h2 class="text-xl font-semibold mb-4 text-text-primary font-display">Modifier la liste</h2>
        <form @submit.prevent="handleUpdateList" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2 text-text-primary font-display">Nom de la liste</label>
            <input
              v-model="editingList.name"
              type="text"
              required
              class="input-field"
            />
          </div>
          <div>
            <label class="block text-sm font-medium mb-2 text-text-primary font-display">Visibilité</label>
            <select
              v-model="editingList.visibility"
              class="input-field"
            >
              <option value="private">Privée</option>
              <option value="friends">Amis uniquement</option>
              <option value="public">Publique</option>
            </select>
          </div>
          <div class="flex space-x-3">
            <button
              type="submit"
              :disabled="isLoading"
              class="btn-primary"
            >
              {{ isLoading ? 'Enregistrement...' : 'Enregistrer les modifications' }}
            </button>
            <button
              type="button"
              @click="editingList = null"
              class="px-4 py-2 rounded-lg bg-bg-tertiary text-text-primary hover:bg-bg-secondary transition-colors font-medium"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="lists.length === 0 && !isLoading" class="glass rounded-xl p-12 text-center border border-border-color">
      <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-accent/10 flex items-center justify-center">
        <span class="text-3xl">📋</span>
      </div>
      <h3 class="text-xl font-semibold text-text-primary font-display mb-2">Aucune liste pour le moment</h3>
      <p class="text-text-secondary font-body mb-4">Créez votre première liste pour commencer à organiser vos médias !</p>
      <button
        @click="showCreateForm = true"
        class="btn-primary"
      >
        Créer une liste
      </button>
    </div>
  </div>
</template>
