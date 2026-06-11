<script setup lang="ts">
import { MediaType, type Media } from '~/types/media'
import { resolveMediaImage } from '~/composables/useMediaCover'

useHead({
  title: "Artiverse - Détails du média",
  meta: [
    { name: "Page de détails d'un média", content: "Détails d'un média"}
  ]
})

const route = useRoute()
const mediaId = route.params.id as string

const { fetchWithAuth, getErrorMessage, isLoading, error, clearError } = useApi()
const { user, isAuthenticated } = useAuth()
const { getSuggestions } = useMedia()
const { getAllLists, addMediaToList } = useLists()

const media = ref<Media | null>(null)
const suggestions = ref<Media[]>([])
const reviews = ref<any[]>([])
const userRating = ref<any>(null)
const newReview = reactive({ title: '', content: '', spoiler: false })
const newRating = ref(0)
const isSubmittingReview = ref(false)
const isSubmittingRating = ref(false)
const reviewError = ref('')

// Existing review by the current user (detected after load)
const existingReview = ref<any>(null)

function initFormFromExisting() {
  if (!user.value) return
  const mine = reviews.value.find(r => r.user_id === user.value!.id)
  if (mine) {
    existingReview.value = mine
    newReview.title = mine.title
    newReview.content = mine.content
    newReview.spoiler = mine.spoiler
  }
  if (userRating.value?.score) {
    newRating.value = userRating.value.score
  }
}

// Add to list
const userLists = ref<any[]>([])
const showListDropdown = ref(false)
const listMessage = ref('')
const listMessageType = ref<'success' | 'error'>('success')

async function loadUserLists() {
  if (!isAuthenticated.value) return
  try {
    userLists.value = await getAllLists()
  } catch {}
}

async function handleAddToList(listId: string, listName: string) {
  try {
    await addMediaToList(listId, mediaId)
    listMessage.value = `Ajouté à "${listName}" !`
    listMessageType.value = 'success'
  } catch {
    listMessage.value = 'Déjà dans cette liste ou erreur.'
    listMessageType.value = 'error'
  } finally {
    showListDropdown.value = false
    setTimeout(() => { listMessage.value = '' }, 3000)
  }
}

const coverImage = computed(() =>
  resolveMediaImage(media.value?.image, media.value?.type)
)

async function fetchMediaDetails() {
  try {
    clearError()
    const [mediaData, reviewsData, suggestionsData] = await Promise.all([
      $fetch<Media>(`/api/media/${mediaId}`),
      $fetch(`/api/v1/reviews/media/${mediaId}`),
      getSuggestions(mediaId, 8),
    ])
    media.value = mediaData
    reviews.value = reviewsData?.items || []
    suggestions.value = suggestionsData?.items || []

    if (isAuthenticated.value) {
      try {
        userRating.value = await fetchWithAuth(`/api/v1/ratings/media/${mediaId}/me`)
      } catch {
        userRating.value = null
      } finally {
        clearError()
      }
    }
    initFormFromExisting()
  } catch (err: any) {
    error.value = err
  }
}

async function submitRatingAndReview() {
  if (!isAuthenticated.value) return
  if (newRating.value < 1 || newRating.value > 10) {
    reviewError.value = 'Veuillez choisir une note entre 1 et 10.'
    return
  }

  const titleFilled = newReview.title.trim()
  const contentFilled = newReview.content.trim()
  const hasReview = titleFilled && contentFilled
  if ((titleFilled || contentFilled) && !hasReview) {
    reviewError.value = 'Veuillez remplir à la fois le titre et le contenu de l\'avis.'
    return
  }

  reviewError.value = ''
  isSubmittingRating.value = true
  isSubmittingReview.value = !!hasReview

  try {
    // Note
    await fetchWithAuth('/api/v1/ratings', {
      method: 'POST',
      body: { media_id: mediaId, score: newRating.value }
    })
    userRating.value = { score: newRating.value }

    // Avis : PATCH si existant, POST sinon
    if (hasReview) {
      if (existingReview.value) {
        const updated = await fetchWithAuth(`/api/v1/reviews/${existingReview.value.id}`, {
          method: 'PATCH',
          body: { title: newReview.title, content: newReview.content, spoiler: newReview.spoiler }
        })
        const idx = reviews.value.findIndex(r => r.id === existingReview.value.id)
        if (idx !== -1) reviews.value[idx] = { ...reviews.value[idx], ...updated }
        existingReview.value = { ...existingReview.value, ...updated }
      } else {
        const review = await fetchWithAuth('/api/v1/reviews', {
          method: 'POST',
          body: { media_id: mediaId, title: newReview.title, content: newReview.content, spoiler: newReview.spoiler }
        })
        review.username = user.value?.username
        review.score = newRating.value
        reviews.value.unshift(review)
        existingReview.value = review
      }
    }
  } catch (err: any) {
    reviewError.value = getErrorMessage(err)
  } finally {
    isSubmittingRating.value = false
    isSubmittingReview.value = false
  }
}

onMounted(async () => {
  await Promise.all([fetchMediaDetails(), loadUserLists()])
  document.addEventListener('click', (e) => {
    const target = e.target as HTMLElement
    if (!target.closest('.list-dropdown-anchor')) {
      showListDropdown.value = false
    }
  })
})

const formattedDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getMediaTypeLabel = (type?: string) => {
  const labels: Record<string, string> = {
    movie: 'Film',
    tv_series: 'Série',
    video_game: 'Jeu vidéo',
    book: 'Livre',
  }
  return type ? labels[type] || type : ''
}
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-5xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">
    <div v-if="isLoading" class="flex items-center justify-center py-20">
      <div class="h-12 w-12 animate-spin rounded-full border-b-2 border-accent"></div>
      <p class="ml-3 text-text-secondary">Chargement...</p>
    </div>

    <div v-else-if="error" class="glass rounded-xl border border-red-500/30 p-6">
      <div class="flex items-start gap-4">
        <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-red-500/20">
          <span class="text-red-400">⚠️</span>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-medium text-red-400">Erreur de chargement</h3>
          <p class="mt-2 text-sm text-red-300">{{ getErrorMessage(error) }}</p>
          <NuxtLink to="/" class="btn-primary mt-4 inline-flex items-center px-4 py-2 text-sm">
            Retour à l'accueil
          </NuxtLink>
        </div>
      </div>
    </div>

    <div v-else-if="media" class="space-y-8">
      <div class="glass rounded-xl p-6 sm:p-8 lg:p-10">
        <div class="grid gap-8 md:grid-cols-3">
          <div class="md:col-span-1">
            <img
              :src="coverImage"
              :alt="media.title"
              class="w-full rounded-lg object-cover shadow-md"
            />
          </div>

          <div class="md:col-span-2">
            <h1 class="mb-4 text-3xl font-extrabold text-text-primary sm:text-4xl">{{ media.title }}</h1>

            <div class="mb-6 flex flex-wrap gap-2">
              <span
                v-if="media.type"
                class="rounded-md bg-accent/20 px-3 py-1 text-sm font-semibold text-accent"
              >
                {{ getMediaTypeLabel(media.type) }}
              </span>
              <span v-if="media.releaseDate" class="rounded-md bg-bg-tertiary px-3 py-1 text-sm text-text-secondary">
                {{ new Date(media.releaseDate).getFullYear() }}
              </span>
              <span v-if="media.rating" class="rounded-md bg-yellow-500/20 px-3 py-1 text-sm font-semibold text-yellow-400">
                ⭐ {{ media.rating }}/10
              </span>
              <!-- User rating indicator -->
              <span v-if="userRating" class="rounded-md bg-emerald-500/20 px-3 py-1 text-sm font-semibold text-emerald-400 border border-emerald-500/30">
                ✓ Votre note : {{ userRating?.score }}/10
              </span>
            </div>

            <p v-if="media.description" class="mb-6 text-text-secondary">
              {{ media.description }}
            </p>

            <div class="flex flex-wrap items-center gap-3">
              <NuxtLink
                to="/explore"
                class="inline-flex items-center rounded-md bg-bg-tertiary px-4 py-2 text-sm font-medium text-text-primary transition-colors hover:bg-border-color"
              >
                ← Retour au catalogue
              </NuxtLink>

              <!-- Ajouter à une liste -->
              <div v-if="isAuthenticated" class="relative list-dropdown-anchor">
                <button
                  @click="showListDropdown = !showListDropdown"
                  class="inline-flex items-center gap-2 rounded-md bg-accent/20 border border-accent/30 px-4 py-2 text-sm font-medium text-accent transition-colors hover:bg-accent/30"
                >
                  <span>+ Ajouter à une liste</span>
                </button>
                <div
                  v-if="showListDropdown"
                  class="absolute left-0 top-full mt-1 z-30 w-56 rounded-xl glass border border-border-color shadow-xl"
                >
                  <div v-if="userLists.length === 0" class="px-4 py-3 text-sm text-text-secondary">
                    Aucune liste.
                    <NuxtLink to="/mylists" class="text-accent hover:underline ml-1">Créer une liste</NuxtLink>
                  </div>
                  <template v-else>
                    <button
                      v-for="list in userLists"
                      :key="list.id"
                      @click="handleAddToList(list.id, list.name)"
                      class="w-full px-4 py-2.5 text-left text-sm text-text-primary hover:bg-bg-tertiary transition-colors first:rounded-t-xl last:rounded-b-xl"
                    >
                      {{ list.name }}
                      <span class="ml-1 text-xs text-text-tertiary">({{ list.items?.length ?? 0 }})</span>
                    </button>
                  </template>
                </div>
              </div>
            </div>

            <!-- Feedback message -->
            <div
              v-if="listMessage"
              :class="[
                'mt-3 rounded-lg px-4 py-2 text-sm font-medium',
                listMessageType === 'success'
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-red-500/20 text-red-300 border border-red-500/30'
              ]"
            >
              {{ listMessage }}
            </div>
          </div>
        </div>
      </div>

      <!-- ===== AVIS + NOTE ===== -->
      <div class="glass rounded-xl p-6 sm:p-8">
        <h2 class="mb-6 text-2xl font-bold text-text-primary">Avis</h2>

        <!-- Formulaire connecté : note + avis ensemble -->
        <div v-if="isAuthenticated" class="mb-8 rounded-xl border border-border-color bg-bg-tertiary/30 p-5 space-y-5">
          <h3 class="text-base font-semibold text-text-primary">
            {{ (userRating || existingReview) ? 'Modifier votre évaluation' : 'Évaluer ce média' }}
          </h3>

          <!-- Note -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-text-secondary">Note</label>
              <span class="text-xl font-bold text-accent font-display">{{ newRating || (userRating?.score ?? 0) }}/10</span>
            </div>
            <input
              v-model.number="newRating"
              type="range" min="1" max="10" step="1"
              class="w-full h-3 rounded-full appearance-none bg-bg-tertiary cursor-pointer"
              :class="(newRating || userRating?.score) >= 8 ? 'accent-green-500' : (newRating || userRating?.score) >= 6 ? 'accent-yellow-500' : 'accent-red-500'"
            />
            <div class="flex justify-between text-xs text-text-tertiary font-medium">
              <span v-for="n in 10" :key="n">{{ n }}</span>
            </div>
            <div class="flex items-center justify-between text-xs">
              <span class="text-red-400 font-medium">Mauvais</span>
              <span class="text-yellow-400 font-medium">Moyen</span>
              <span class="text-green-400 font-medium">Excellent</span>
            </div>
          </div>

          <!-- Avis (titre + contenu + spoiler) -->
          <div class="space-y-3 border-t border-border-color pt-4">
            <p class="text-sm text-text-secondary">Ajouter un avis <span class="text-text-tertiary">(optionnel)</span></p>
            <input
              v-model="newReview.title"
              type="text"
              placeholder="Titre de votre avis"
              class="block w-full rounded-lg border border-border-color bg-bg-secondary px-3 py-2 text-sm text-text-primary placeholder-text-tertiary outline-none focus:border-accent"
            />
            <textarea
              v-model="newReview.content"
              rows="3"
              placeholder="Partagez votre opinion..."
              class="block w-full rounded-lg border border-border-color bg-bg-secondary px-3 py-2 text-sm text-text-primary placeholder-text-tertiary outline-none focus:border-accent resize-none"
            ></textarea>
            <label class="flex items-center gap-2 cursor-pointer select-none">
              <input v-model="newReview.spoiler" type="checkbox" class="h-4 w-4 rounded border-border-color" />
              <span class="text-sm text-text-secondary">Contient des spoilers</span>
            </label>
          </div>

          <div v-if="reviewError" class="rounded-lg bg-red-500/10 border border-red-500/30 px-4 py-2">
            <p class="text-sm text-red-400">{{ reviewError }}</p>
          </div>

          <!-- Actions -->
          <div class="flex gap-2 pt-1">
            <button
              @click="submitRatingAndReview"
              :disabled="isSubmittingRating || isSubmittingReview"
              class="btn-primary px-5 py-2.5 text-sm disabled:opacity-50"
            >
              {{ (isSubmittingRating || isSubmittingReview) ? 'Publication...' : (userRating ? 'Mettre à jour' : 'Publier') }}
            </button>
          </div>
        </div>

        <div v-else class="mb-6 rounded-xl border border-border-color bg-bg-tertiary/30 px-5 py-4 text-sm text-text-secondary">
          <NuxtLink to="/users/login" class="text-accent hover:text-accent-hover font-medium">Connectez-vous</NuxtLink>
          pour noter ce média et laisser un avis.
        </div>

        <!-- Liste des avis -->
        <div v-if="reviews.length > 0" class="space-y-4">
          <div
            v-for="review in reviews"
            :key="review.id"
            class="rounded-lg border border-border-color bg-bg-tertiary/30 p-4"
          >
            <div class="mb-1 flex items-start justify-between gap-2">
              <h4 class="font-semibold text-text-primary">{{ review.title }}</h4>
              <div class="flex items-center gap-2 shrink-0">
                <span v-if="review.score" class="rounded-md bg-yellow-500/20 px-2 py-0.5 text-xs font-bold text-yellow-400">
                  ⭐ {{ review.score }}/10
                </span>
                <span class="text-xs text-text-tertiary">{{ formattedDate(review.created_at) }}</span>
              </div>
            </div>
            <p class="text-sm text-text-secondary">{{ review.content }}</p>
            <div class="mt-2 flex items-center gap-2">
              <span v-if="review.username" class="text-xs font-medium text-accent">{{ review.username }}</span>
              <span v-if="review.spoiler" class="rounded-md bg-yellow-500/20 px-2 py-0.5 text-xs font-semibold text-yellow-400">⚠️ Spoiler</span>
            </div>
          </div>
        </div>
        <div v-else class="py-8 text-center text-sm text-text-tertiary">
          Aucun avis pour l'instant. Soyez le premier !
        </div>
      </div>

      <!-- ===== SUGGESTIONS ===== -->
      <div v-if="suggestions.length > 0" class="glass rounded-xl p-6 sm:p-8">
        <h2 class="mb-6 text-2xl font-bold text-text-primary">Vous aimerez aussi</h2>
        <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          <NuxtLink
            v-for="item in suggestions"
            :key="item.id"
            :to="`/media/${item.id}`"
            class="group overflow-hidden rounded-lg bg-bg-tertiary/50 transition-transform hover:scale-[1.02]"
          >
            <div class="aspect-[2/3] overflow-hidden">
              <img
                :src="resolveMediaImage(item.image, item.type)"
                :alt="item.title"
                class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
            </div>
            <div class="p-3">
              <p class="line-clamp-2 text-sm font-semibold text-text-primary group-hover:text-accent">{{ item.title }}</p>
              <p class="mt-1 text-xs text-text-tertiary">{{ getMediaTypeLabel(item.type) }}</p>
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>
