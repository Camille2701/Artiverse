<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useMedia } from '~/composables/useMedia'
import type { Media, MediaCreate } from '~/types/media'

const { getAllMedia, createMedia, updateMedia, deleteMedia } = useMedia()

const mediaList = ref<Media[]>([])
const isLoading = ref(false)
const showCreateForm = ref(false)
const editingMedia = ref<Media | null>(null)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const activeTab = ref<'list' | 'import'>('list')

const createForm = ref<MediaCreate>({
  media_type: 'movie' as any,
  title: '',
  synopsis: '',
  release_date: ''
})

const searchQuery = ref('')

// Import state
const importSource = ref<'sample' | 'tmdb' | 'rawg'>('sample')
const importApiKey = ref('')
const importLimit = ref(50)
const importLoading = ref(false)
const importResult = ref<{ success: number; skipped: number; error: number; total: number; message: string } | null>(null)

const importSources = [
  { value: 'sample', label: '🎲 Données exemples', needsKey: false, description: 'Importe ~9 médias de démonstration (films, séries, jeux, livres).' },
  { value: 'tmdb', label: '🎬 TMDb (Films & Séries)', needsKey: true, description: 'Importe des films et séries populaires depuis The Movie Database.' },
  { value: 'rawg', label: '🎮 RAWG (Jeux vidéo)', needsKey: true, description: 'Importe des jeux vidéo populaires depuis RAWG.' },
]

const currentSource = computed(() => importSources.find(s => s.value === importSource.value))

onMounted(async () => {
  await loadMedia()
})

async function loadMedia() {
  try {
    isLoading.value = true
    const data = await getAllMedia({ limit: 50 })
    mediaList.value = data.items
  } catch {
    showMessage('Impossible de charger les médias', 'error')
  } finally {
    isLoading.value = false
  }
}

async function handleCreateMedia() {
  try {
    isLoading.value = true
    await createMedia(createForm.value)
    showMessage('Média créé avec succès !', 'success')
    showCreateForm.value = false
    createForm.value = { media_type: 'movie' as any, title: '', synopsis: '', release_date: '' }
    await loadMedia()
  } catch (error: any) {
    showMessage(error.message || 'Échec de la création', 'error')
  } finally {
    isLoading.value = false
  }
}

async function handleUpdateMedia() {
  if (!editingMedia.value) return
  try {
    isLoading.value = true
    await updateMedia(editingMedia.value.id, {
      title: editingMedia.value.title,
      synopsis: editingMedia.value.synopsis
    })
    showMessage('Média mis à jour !', 'success')
    editingMedia.value = null
    await loadMedia()
  } catch (error: any) {
    showMessage(error.message || 'Échec de la mise à jour', 'error')
  } finally {
    isLoading.value = false
  }
}

async function handleDeleteMedia(id: string) {
  if (!confirm('Supprimer ce média ?')) return
  try {
    isLoading.value = true
    await deleteMedia(id)
    showMessage('Média supprimé !', 'success')
    await loadMedia()
  } catch (error: any) {
    showMessage(error.message || 'Échec de la suppression', 'error')
  } finally {
    isLoading.value = false
  }
}

async function handleImport() {
  importLoading.value = true
  importResult.value = null
  try {
    const body: any = { source: importSource.value, limit: importLimit.value }
    if (currentSource.value?.needsKey) {
      body.api_key = importApiKey.value
    }

    const result = await $fetch<{ success: number; skipped: number; error: number; total: number; message: string }>(
      '/api/v1/admin/import',
      { method: 'POST', body }
    )
    importResult.value = result
    await loadMedia()
  } catch (error: any) {
    importResult.value = {
      success: 0, skipped: 0, error: 1, total: 0,
      message: error.data?.detail || error.message || "L'importation a échoué"
    }
  } finally {
    importLoading.value = false
  }
}

function showMessage(msg: string, type: 'success' | 'error') {
  message.value = msg
  messageType.value = type
  setTimeout(() => { message.value = '' }, 4000)
}

const filteredMedia = computed(() => {
  if (!searchQuery.value) return mediaList.value
  const q = searchQuery.value.toLowerCase()
  return mediaList.value.filter(m => m.title.toLowerCase().includes(q))
})
</script>

<template>
  <div class="mx-auto max-w-6xl p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-text-primary font-display">Gestion des médias</h1>
        <p class="text-sm text-text-secondary mt-1">{{ mediaList.length }} médias dans la base</p>
      </div>
      <div class="flex items-center gap-2">
        <button
          v-if="activeTab === 'list'"
          @click="showCreateForm = !showCreateForm"
          class="rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-accent-hover"
        >
          {{ showCreateForm ? 'Annuler' : '+ Nouveau média' }}
        </button>
      </div>
    </div>

    <!-- Alert message -->
    <Transition enter-active-class="transition duration-200" enter-from-class="opacity-0 -translate-y-2" leave-active-class="transition duration-150" leave-to-class="opacity-0">
      <div v-if="message" :class="[
        'rounded-xl p-4 text-sm font-medium border',
        messageType === 'success'
          ? 'bg-green-500/10 text-green-400 border-green-500/30'
          : 'bg-red-500/10 text-red-400 border-red-500/30'
      ]">
        {{ message }}
      </div>
    </Transition>

    <!-- Tabs -->
    <div class="flex items-center gap-1 rounded-xl bg-bg-tertiary/40 p-1 w-fit">
      <button
        @click="activeTab = 'list'"
        :class="['px-4 py-2 rounded-lg text-sm font-medium transition-all', activeTab === 'list' ? 'bg-accent text-white shadow' : 'text-text-secondary hover:text-text-primary']"
      >
        📋 Liste des médias
      </button>
      <button
        @click="activeTab = 'import'"
        :class="['px-4 py-2 rounded-lg text-sm font-medium transition-all', activeTab === 'import' ? 'bg-accent text-white shadow' : 'text-text-secondary hover:text-text-primary']"
      >
        📥 Importer des médias
      </button>
    </div>

    <!-- ===== LIST TAB ===== -->
    <template v-if="activeTab === 'list'">
      <!-- Create Form -->
      <div v-if="showCreateForm" class="glass rounded-xl p-6 border border-border-color">
        <h2 class="text-lg font-semibold text-text-primary mb-4 font-display">Créer un nouveau média</h2>
        <form @submit.prevent="handleCreateMedia" class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1">Type</label>
            <select v-model="createForm.media_type" required
              class="w-full rounded-lg border border-border-color bg-bg-secondary px-3 py-2 text-sm text-text-primary focus:border-accent focus:outline-none">
              <option value="movie">Film</option>
              <option value="tv_series">Série TV</option>
              <option value="video_game">Jeu vidéo</option>
              <option value="book">Livre</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1">Titre</label>
            <input v-model="createForm.title" type="text" required
              class="w-full rounded-lg border border-border-color bg-bg-secondary px-3 py-2 text-sm text-text-primary focus:border-accent focus:outline-none" />
          </div>
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-text-secondary mb-1">Synopsis</label>
            <textarea v-model="createForm.synopsis" rows="3"
              class="w-full rounded-lg border border-border-color bg-bg-secondary px-3 py-2 text-sm text-text-primary focus:border-accent focus:outline-none"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1">Date de sortie</label>
            <input v-model="createForm.release_date" type="date"
              class="w-full rounded-lg border border-border-color bg-bg-secondary px-3 py-2 text-sm text-text-primary focus:border-accent focus:outline-none" />
          </div>
          <div class="flex items-end">
            <button type="submit" :disabled="isLoading"
              class="rounded-lg bg-accent px-6 py-2 text-sm font-semibold text-white transition-colors hover:bg-accent-hover disabled:opacity-50">
              {{ isLoading ? 'Création...' : 'Créer' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Search -->
      <div>
        <input v-model="searchQuery" type="text" placeholder="Rechercher un média..."
          class="w-full rounded-xl border border-border-color bg-bg-secondary px-4 py-2.5 text-sm text-text-primary placeholder-text-tertiary focus:border-accent focus:outline-none" />
      </div>

      <!-- Media Table -->
      <div class="glass rounded-xl border border-border-color overflow-hidden">
        <div v-if="isLoading" class="flex justify-center py-10">
          <div class="spinner !h-8 !w-8 !border-3"></div>
        </div>
        <table v-else class="min-w-full">
          <thead class="border-b border-border-color bg-bg-tertiary/30">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-text-tertiary">Titre</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-text-tertiary">Type</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-text-tertiary">Note</th>
              <th class="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-text-tertiary">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border-color">
            <tr v-for="media in filteredMedia" :key="media.id" class="transition-colors hover:bg-bg-tertiary/20">
              <td class="px-6 py-4 text-sm font-medium text-text-primary">{{ media.title }}</td>
              <td class="px-6 py-4 text-sm capitalize text-text-secondary">{{ (media as any).type ?? media.media_type }}</td>
              <td class="px-6 py-4 text-sm text-text-secondary">{{ ((media as any).rating ?? media.average_rating)?.toFixed(1) }}</td>
              <td class="px-6 py-4 text-right text-sm">
                <button @click="editingMedia = media"
                  class="mr-3 font-medium text-accent hover:text-accent-hover transition-colors">Modifier</button>
                <button @click="handleDeleteMedia(media.id)"
                  class="font-medium text-red-500 hover:text-red-400 transition-colors">Supprimer</button>
              </td>
            </tr>
            <tr v-if="filteredMedia.length === 0">
              <td colspan="4" class="px-6 py-10 text-center text-sm text-text-tertiary">Aucun média trouvé</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- ===== IMPORT TAB ===== -->
    <template v-if="activeTab === 'import'">
      <div class="glass rounded-xl p-6 border border-border-color space-y-6">
        <div>
          <h2 class="text-lg font-semibold text-text-primary font-display mb-1">Importer des médias</h2>
          <p class="text-sm text-text-secondary">Enrichissez votre catalogue en important depuis des sources externes.</p>
        </div>

        <!-- Source selector -->
        <div>
          <label class="block text-sm font-medium text-text-secondary mb-2">Source</label>
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <button
              v-for="src in importSources"
              :key="src.value"
              @click="importSource = src.value as any"
              :class="[
                'rounded-xl border p-4 text-left transition-all',
                importSource === src.value
                  ? 'border-accent bg-accent/10 text-text-primary'
                  : 'border-border-color bg-bg-secondary text-text-secondary hover:border-border-color-light'
              ]"
            >
              <div class="font-semibold text-sm mb-1">{{ src.label }}</div>
              <div class="text-xs leading-relaxed opacity-75">{{ src.description }}</div>
            </button>
          </div>
        </div>

        <!-- API Key (only when needed) -->
        <div v-if="currentSource?.needsKey">
          <label class="block text-sm font-medium text-text-secondary mb-1">
            Clé API <span class="text-accent">*</span>
          </label>
          <input
            v-model="importApiKey"
            type="password"
            :placeholder="`Clé API ${currentSource.label}`"
            class="w-full rounded-xl border border-border-color bg-bg-secondary px-4 py-2.5 text-sm text-text-primary placeholder-text-tertiary focus:border-accent focus:outline-none"
          />
          <p v-if="importSource === 'tmdb'" class="mt-1.5 text-xs text-text-tertiary">
            Obtenez une clé gratuite sur <span class="text-accent">themoviedb.org/settings/api</span>
          </p>
          <p v-else-if="importSource === 'rawg'" class="mt-1.5 text-xs text-text-tertiary">
            Obtenez une clé gratuite sur <span class="text-accent">rawg.io/docs</span>
          </p>
        </div>

        <!-- Limit -->
        <div v-if="importSource !== 'sample'">
          <label class="block text-sm font-medium text-text-secondary mb-1">Nombre de médias</label>
          <input v-model.number="importLimit" type="number" min="1" max="200"
            class="w-40 rounded-xl border border-border-color bg-bg-secondary px-4 py-2.5 text-sm text-text-primary focus:border-accent focus:outline-none" />
        </div>

        <!-- Import button -->
        <button
          @click="handleImport"
          :disabled="importLoading || (currentSource?.needsKey && !importApiKey)"
          class="flex items-center gap-2 rounded-xl bg-accent px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-accent-hover disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg v-if="importLoading" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {{ importLoading ? 'Importation...' : 'Lancer l\'importation' }}
        </button>

        <!-- Import result -->
        <div v-if="importResult" :class="[
          'rounded-xl p-5 border',
          importResult.error > 0 && importResult.success === 0
            ? 'border-red-500/30 bg-red-500/10'
            : 'border-green-500/30 bg-green-500/10'
        ]">
          <p class="font-semibold text-sm mb-3" :class="importResult.error > 0 && importResult.success === 0 ? 'text-red-400' : 'text-green-400'">
            {{ importResult.message }}
          </p>
          <div class="grid grid-cols-3 gap-3 text-center">
            <div class="rounded-lg bg-bg-secondary/50 p-3">
              <div class="text-2xl font-bold text-green-400">{{ importResult.success }}</div>
              <div class="text-xs text-text-secondary mt-1">Ajoutés</div>
            </div>
            <div class="rounded-lg bg-bg-secondary/50 p-3">
              <div class="text-2xl font-bold text-yellow-400">{{ importResult.skipped }}</div>
              <div class="text-xs text-text-secondary mt-1">Ignorés</div>
            </div>
            <div class="rounded-lg bg-bg-secondary/50 p-3">
              <div class="text-2xl font-bold text-red-400">{{ importResult.error }}</div>
              <div class="text-xs text-text-secondary mt-1">Erreurs</div>
            </div>
          </div>
        </div>

        <!-- CLI instructions -->
        <div class="rounded-xl border border-border-color bg-bg-tertiary/20 p-5">
          <h3 class="text-sm font-semibold text-text-primary mb-3">Importer en ligne de commande (Docker)</h3>
          <div class="space-y-2 text-xs font-mono text-text-secondary">
            <div class="rounded-lg bg-bg-secondary px-3 py-2">
              docker compose exec backend python -m app.import_media --sample
            </div>
            <div class="rounded-lg bg-bg-secondary px-3 py-2">
              docker compose exec backend python -m app.import_media --source tmdb --api-key YOUR_KEY --limit 100
            </div>
            <div class="rounded-lg bg-bg-secondary px-3 py-2">
              docker compose exec backend python -m app.import_media --source rawg --api-key YOUR_KEY --limit 50
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Edit Modal -->
    <Teleport to="body">
      <div v-if="editingMedia" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
        <div class="glass w-full max-w-md rounded-2xl border border-border-color p-6 mx-4 shadow-2xl">
          <h2 class="text-xl font-semibold text-text-primary mb-5 font-display">Modifier le média</h2>
          <form @submit.prevent="handleUpdateMedia" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-text-secondary mb-1">Titre</label>
              <input v-model="editingMedia.title" type="text" required
                class="w-full rounded-xl border border-border-color bg-bg-secondary px-4 py-2.5 text-sm text-text-primary focus:border-accent focus:outline-none" />
            </div>
            <div>
              <label class="block text-sm font-medium text-text-secondary mb-1">Synopsis</label>
              <textarea v-model="editingMedia.synopsis" rows="4"
                class="w-full rounded-xl border border-border-color bg-bg-secondary px-4 py-2.5 text-sm text-text-primary focus:border-accent focus:outline-none"></textarea>
            </div>
            <div class="flex gap-3 pt-2">
              <button type="submit" :disabled="isLoading"
                class="flex-1 rounded-xl bg-accent py-2.5 text-sm font-semibold text-white transition-colors hover:bg-accent-hover disabled:opacity-50">
                {{ isLoading ? 'Sauvegarde...' : 'Sauvegarder' }}
              </button>
              <button type="button" @click="editingMedia = null"
                class="flex-1 rounded-xl border border-border-color bg-bg-secondary py-2.5 text-sm font-semibold text-text-secondary transition-colors hover:bg-bg-tertiary">
                Annuler
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>
