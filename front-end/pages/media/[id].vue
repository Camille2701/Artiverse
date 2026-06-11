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

const media = ref<Media | null>(null)
const suggestions = ref<Media[]>([])
const reviews = ref<any[]>([])
const userRating = ref<any>(null)
const newReview = reactive({
  title: '',
  content: '',
  spoiler: false
})
const newRating = ref(0)
const isSubmittingReview = ref(false)
const isSubmittingRating = ref(false)
const showReviewForm = ref(false)
const reviewError = ref('')

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
  } catch (err: any) {
    error.value = err
  }
}

async function submitReview() {
  if (!isAuthenticated.value) {
    reviewError.value = 'Vous devez être connecté pour laisser un avis.'
    return
  }

  if (!newReview.title.trim() || !newReview.content.trim()) {
    reviewError.value = 'Veuillez remplir tous les champs.'
    return
  }

  isSubmittingReview.value = true
  reviewError.value = ''

  try {
    const review = await fetchWithAuth('/api/v1/reviews', {
      method: 'POST',
      body: {
        media_id: mediaId,
        title: newReview.title,
        content: newReview.content,
        spoiler: newReview.spoiler
      }
    })

    reviews.value.unshift(review)
    newReview.title = ''
    newReview.content = ''
    newReview.spoiler = false
    showReviewForm.value = false
  } catch (err: any) {
    reviewError.value = getErrorMessage(err)
  } finally {
    isSubmittingReview.value = false
  }
}

async function submitRating() {
  if (!isAuthenticated.value) {
    alert('Vous devez être connecté pour noter ce média.')
    return
  }

  if (newRating.value < 1 || newRating.value > 10) {
    alert('Veuillez noter entre 1 et 10.')
    return
  }

  isSubmittingRating.value = true

  try {
    await fetchWithAuth('/api/v1/ratings', {
      method: 'POST',
      body: {
        media_id: mediaId,
        score: newRating.value
      }
    })

    userRating.value = { score: newRating.value }
    newRating.value = 0
  } catch (err: any) {
    alert(getErrorMessage(err))
  } finally {
    isSubmittingRating.value = false
  }
}

onMounted(fetchMediaDetails)

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
                ✓ Votre note : {{ userRating }}/10
              </span>
            </div>

            <p v-if="media.description" class="mb-6 text-text-secondary">
              {{ media.description }}
            </p>

            <div class="mb-6 rounded-lg bg-bg-tertiary/50 p-4">
              <h3 class="mb-3 font-semibold text-text-primary">Votre note</h3>
              <div v-if="isAuthenticated">
                <div v-if="userRating" class="flex items-center gap-2">
                  <span class="text-lg font-semibold text-yellow-400">⭐ {{ userRating.score }}/10</span>
                  <span class="text-sm text-text-secondary">Vous avez noté ce média</span>
                </div>
                <div v-else class="space-y-4">
                <!-- Already rated indicator -->
                <div v-if="userRating" class="flex items-center gap-3 rounded-lg bg-emerald-500/20 border border-emerald-500/30 px-4 py-3">
                  <div class="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-500/30">
                    <span class="text-emerald-400 text-sm">✓</span>
                  </div>
                  <div class="flex-1">
                    <p class="text-sm font-medium text-emerald-300">Vous avez noté ce média</p>
                    <p class="text-xs text-emerald-400/70">Votre note : {{ userRating }}/10 ⭐</p>
                  </div>
                </div>

                <!-- Rating slider -->
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <label class="text-sm font-medium text-text-secondary">Votre note</label>
                    <span class="text-2xl font-bold text-accent font-display">{{ newRating }}/10</span>
                  </div>

                  <div class="relative">
                    <input
                      v-model.number="newRating"
                      type="range"
                      min="1"
                      max="10"
                      step="1"
                      class="w-full h-3 rounded-full appearance-none bg-bg-tertiary cursor-pointer"
                      :class="newRating >= 8 ? 'accent-green-500' : newRating >= 6 ? 'accent-yellow-500' : 'accent-red-500'"
                    />

                    <!-- Star indicators -->
                    <div class="flex justify-between mt-2 text-xs text-text-tertiary font-medium">
                      <span>1</span>
                      <span>2</span>
                      <span>3</span>
                      <span>4</span>
                      <span>5</span>
                      <span>6</span>
                      <span>7</span>
                      <span>8</span>
                      <span>9</span>
                      <span>10</span>
                    </div>
                  </div>

                  <div class="flex items-center justify-between text-xs">
                    <span class="text-red-400 font-medium">Mauvais</span>
                    <span class="text-yellow-400 font-medium">Moyen</span>
                    <span class="text-green-400 font-medium">Excellent</span>
                  </div>
                </div>

                <button
                  @click="submitRating"
                  :disabled="isSubmittingRating"
                  class="btn-primary w-full px-4 py-3 text-sm disabled:opacity-50"
                >
                  {{ userRating ? 'Mettre à jour la note' : 'Noter ce média' }}
                </button>
              </div>
              </div>
              <div v-else class="text-sm text-text-secondary">
                <NuxtLink to="/users/login" class="text-accent hover:text-accent-hover">Connectez-vous</NuxtLink>
                pour noter ce média.
              </div>
            </div>

            <NuxtLink
              to="/home"
              class="inline-flex items-center rounded-md bg-bg-tertiary px-4 py-2 text-sm font-medium text-text-primary transition-colors hover:bg-border-color"
            >
              ← Retour au catalogue
            </NuxtLink>
          </div>
        </div>
      </div>

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

      <div class="glass rounded-xl p-6 sm:p-8">
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-2xl font-bold text-text-primary">Avis</h2>
          <button
            v-if="isAuthenticated && !showReviewForm"
            @click="showReviewForm = true"
            class="btn-primary px-4 py-2 text-sm"
          >
            + Ajouter un avis
          </button>
        </div>

        <div v-if="showReviewForm" class="mb-6 rounded-lg bg-bg-tertiary/50 p-4">
          <h3 class="mb-4 text-lg font-semibold text-text-primary">Rédiger un avis</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-text-secondary">Titre</label>
              <input
                v-model="newReview.title"
                type="text"
                placeholder="Titre de votre avis"
                class="mt-1 block w-full rounded-md border border-border-color bg-bg-secondary px-3 py-2 text-sm text-text-primary"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-text-secondary">Votre avis</label>
              <textarea
                v-model="newReview.content"
                rows="4"
                placeholder="Partagez votre opinion..."
                class="mt-1 block w-full rounded-md border border-border-color bg-bg-secondary px-3 py-2 text-sm text-text-primary"
              ></textarea>
            </div>
            <div class="flex items-center gap-2">
              <input
                v-model="newReview.spoiler"
                type="checkbox"
                id="spoiler"
                class="h-4 w-4 rounded border-border-color"
              />
              <label for="spoiler" class="text-sm text-text-secondary">Contient des spoilers</label>
            </div>
            <div v-if="reviewError" class="rounded-md bg-red-500/10 p-3">
              <p class="text-sm text-red-400">{{ reviewError }}</p>
            </div>
            <div class="flex gap-2">
              <button
                @click="submitReview"
                :disabled="isSubmittingReview"
                class="btn-primary px-4 py-2 text-sm disabled:opacity-50"
              >
                {{ isSubmittingReview ? 'Publication...' : 'Publier' }}
              </button>
              <button
                @click="showReviewForm = false"
                class="rounded-md border border-border-color px-4 py-2 text-sm font-medium text-text-secondary hover:bg-bg-tertiary"
              >
                Annuler
              </button>
            </div>
          </div>
        </div>

        <div v-if="reviews.length > 0" class="space-y-4">
          <div
            v-for="review in reviews"
            :key="review.id"
            class="rounded-lg border border-border-color bg-bg-tertiary/30 p-4"
          >
            <div class="mb-2 flex items-center justify-between">
              <h4 class="font-semibold text-text-primary">{{ review.title }}</h4>
              <span class="text-sm text-text-tertiary">{{ formattedDate(review.created_at) }}</span>
            </div>
            <p class="text-text-secondary">{{ review.content }}</p>
            <div class="mt-2 flex items-center gap-2">
              <span v-if="review.user" class="text-sm font-medium text-text-secondary">
                {{ review.user.username }}
              </span>
              <span v-if="review.spoiler" class="rounded-md bg-yellow-500/20 px-2 py-0.5 text-xs font-semibold text-yellow-400">
                ⚠️ Spoiler
              </span>
            </div>
          </div>
        </div>

        <div v-else class="py-8 text-center text-text-tertiary">
          Aucun avis pour ce média. Soyez le premier à donner votre avis !
        </div>
      </div>
    </div>
  </div>
</template>
