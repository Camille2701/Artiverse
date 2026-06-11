<script setup lang="ts">
import { useLists } from '~/composables/useLists'
import { resolveMediaImage } from '~/composables/useMediaCover'

const { getListById, removeMediaFromList } = useLists()
const { isAuthenticated } = useAuth()

const route = useRoute()
const listId = route.params.id as string

const list = ref<any>(null)
const enrichedItems = ref<any[]>([])
const isLoading = ref(true)
const removing = ref<string | null>(null)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

const visibilityLabel: Record<string, string> = {
  private: 'Privée',
  friends: 'Amis',
  public: 'Publique',
}

const visibilityColor: Record<string, string> = {
  private: 'bg-bg-tertiary text-text-secondary',
  friends: 'bg-blue-500/20 text-blue-400',
  public: 'bg-emerald-500/20 text-emerald-400',
}

const mediaTypeLabel: Record<string, string> = {
  movie: 'Film',
  tv_series: 'Série',
  video_game: 'Jeu vidéo',
  book: 'Livre',
}

async function loadList() {
  isLoading.value = true
  try {
    list.value = await getListById(listId)
    if (list.value?.items?.length) {
      const results = await Promise.all(
        list.value.items.map((item: any) =>
          $fetch<any>(`/api/v1/media/${item.media_id}`).catch(() => null)
        )
      )
      enrichedItems.value = list.value.items.map((item: any, i: number) => ({
        ...item,
        media: results[i],
      }))
    } else {
      enrichedItems.value = []
    }
  } catch {
    message.value = 'Impossible de charger la liste.'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleRemove(mediaId: string) {
  removing.value = mediaId
  try {
    await removeMediaFromList(listId, mediaId)
    enrichedItems.value = enrichedItems.value.filter(i => i.media_id !== mediaId)
    if (list.value) list.value.items = list.value.items.filter((i: any) => i.media_id !== mediaId)
  } catch {
    message.value = 'Erreur lors de la suppression.'
    messageType.value = 'error'
    setTimeout(() => { message.value = '' }, 3000)
  } finally {
    removing.value = null
  }
}

onMounted(loadList)
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-6xl px-4 py-4 sm:my-6 sm:px-6 lg:my-8 lg:px-8">

    <!-- Loading -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-20">
      <div class="spinner !h-12 !w-12 !border-4"></div>
      <p class="mt-4 text-text-secondary font-body">Chargement...</p>
    </div>

    <div v-else-if="list" class="space-y-8">
      <!-- Header -->
      <div class="glass rounded-2xl p-6 sm:p-8 border border-white/10">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div class="flex items-center gap-3 mb-2">
              <NuxtLink to="/mylists" class="text-text-tertiary hover:text-text-primary transition-colors text-sm">
                ← Mes listes
              </NuxtLink>
            </div>
            <h1 class="text-3xl font-bold text-text-primary font-display">{{ list.name }}</h1>
            <div class="mt-2 flex items-center gap-3">
              <span :class="['px-3 py-1 rounded-full text-xs font-semibold', visibilityColor[list.visibility] ?? visibilityColor.private]">
                {{ visibilityLabel[list.visibility] ?? list.visibility }}
              </span>
              <span class="text-sm text-text-secondary font-body">
                {{ enrichedItems.length }} média{{ enrichedItems.length !== 1 ? 's' : '' }}
              </span>
            </div>
          </div>
          <NuxtLink to="/explore" class="btn-primary px-5 py-2.5 text-sm self-start sm:self-auto">
            + Ajouter des médias
          </NuxtLink>
        </div>
      </div>

      <!-- Alert -->
      <div
        v-if="message"
        :class="[
          'rounded-xl px-5 py-3 text-sm font-medium border',
          messageType === 'success'
            ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
            : 'bg-red-500/20 text-red-300 border-red-500/30'
        ]"
      >
        {{ message }}
      </div>

      <!-- Items grid -->
      <div v-if="enrichedItems.length > 0" class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
        <div
          v-for="item in enrichedItems"
          :key="item.id"
          class="group relative"
        >
          <NuxtLink :to="item.media ? `/media/${item.media_id}` : '#'" class="block">
            <div class="relative overflow-hidden rounded-xl bg-bg-tertiary aspect-[2/3]">
              <img
                :src="resolveMediaImage(item.media?.cover_image ?? item.media?.image, item.media?.media_type ?? item.media?.type)"
                :alt="item.media?.title ?? 'Média'"
                class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
              <!-- Gradient overlay -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <!-- Type badge -->
              <div v-if="item.media" class="absolute top-2 left-2">
                <span class="px-2 py-0.5 rounded-md text-xs font-semibold bg-black/60 text-white backdrop-blur-sm">
                  {{ mediaTypeLabel[item.media.media_type ?? item.media.type] ?? '' }}
                </span>
              </div>
            </div>
          </NuxtLink>

          <!-- Info + remove -->
          <div class="mt-2 px-0.5">
            <p class="line-clamp-1 text-sm font-semibold text-text-primary font-display" :title="item.media?.title">
              {{ item.media?.title ?? '...' }}
            </p>
            <div class="mt-1 flex items-center justify-between">
              <span class="text-xs text-text-tertiary font-body">
                {{ new Date(item.created_at).toLocaleDateString('fr-FR') }}
              </span>
              <button
                v-if="isAuthenticated"
                @click="handleRemove(item.media_id)"
                :disabled="removing === item.media_id"
                class="text-xs text-red-400 hover:text-red-300 transition-colors disabled:opacity-50"
                title="Retirer de la liste"
              >
                {{ removing === item.media_id ? '...' : 'Retirer' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="glass rounded-xl p-12 text-center border border-border-color">
        <div class="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-bg-tertiary text-4xl">
          📋
        </div>
        <h3 class="mb-2 text-xl font-semibold text-text-primary font-display">Liste vide</h3>
        <p class="mb-6 text-sm text-text-secondary font-body">Ajoutez des médias depuis leur page de détail.</p>
        <NuxtLink to="/explore" class="btn-primary px-6 py-2.5">Parcourir le catalogue</NuxtLink>
      </div>
    </div>

    <!-- List not found -->
    <div v-else class="glass rounded-xl p-12 text-center border border-border-color">
      <p class="text-text-secondary font-body">Liste introuvable.</p>
      <NuxtLink to="/mylists" class="btn-primary mt-4 inline-block px-6 py-2.5">Mes listes</NuxtLink>
    </div>
  </div>
</template>
