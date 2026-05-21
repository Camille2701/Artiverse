<script setup lang="ts">
import { MediaType, type Media } from '~/types/media'

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

const media = ref<Media | null>(null)
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

async function fetchMediaDetails() {
  try {
    clearError()
    const [mediaData, reviewsData] = await Promise.all([
      $fetch<Media>(`/api/media/${mediaId}`),
      $fetch(`/api/v1/reviews/media/${mediaId}`)
    ])
    media.value = mediaData
    reviews.value = reviewsData?.items || []

    // Fetch user rating if authenticated
    if (isAuthenticated.value) {
      try {
        userRating.value = await fetchWithAuth(`/api/v1/ratings/${mediaId}`)
      } catch (err) {
        // User hasn't rated this media yet
        userRating.value = null
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

const averageRating = computed(() => {
  if (!reviews.value.length) return media.value?.rating || 0
  const total = reviews.value.reduce((sum, r) => sum + (r.rating || 0), 0)
  return (total / reviews.value.length).toFixed(1)
})

const formattedDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-5xl px-4 py-4 sm:my-6 sm:px-6 sm:py-6 lg:my-8 lg:px-8 lg:py-8">
    <div v-if="isLoading" class="flex items-center justify-center py-20">
      <div class="h-12 w-12 animate-spin rounded-full border-b-2 border-accent"></div>
      <p class="ml-3 text-gray-600">Chargement...</p>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-6">
      <div class="flex items-start gap-4">
        <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-red-100">
          <span class="text-red-600">⚠️</span>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-medium text-red-800">Erreur de chargement</h3>
          <p class="mt-2 text-sm text-red-700">{{ getErrorMessage(error) }}</p>
          <NuxtLink
            to="/"
            class="mt-4 inline-flex items-center rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1"
          >
            Retour à l'accueil
          </NuxtLink>
        </div>
      </div>
    </div>

    <div v-else-if="media" class="space-y-8">
      <!-- Media Details -->
      <div class="rounded-xl bg-white p-6 shadow-lg sm:p-8 lg:p-10">
        <div class="grid gap-8 md:grid-cols-3">
          <div class="md:col-span-1">
            <img
              :src="media.image || 'https://via.placeholder.com/400x600'"
              :alt="media.title"
              class="w-full rounded-lg object-cover shadow-md"
            />
          </div>

          <div class="md:col-span-2">
            <h1 class="mb-4 text-3xl font-extrabold text-gray-900 sm:text-4xl">{{ media.title }}</h1>

            <div class="mb-6 flex flex-wrap gap-2">
              <span
                v-if="media.type"
                class="rounded-md bg-blue-100 px-3 py-1 text-sm font-semibold text-blue-800"
              >
                {{ media.type === 'movie' ? 'Film' : media.type === 'tv_series' ? 'Série' : media.type === 'video_game' ? 'Jeu vidéo' : 'Livre' }}
              </span>
              <span v-if="media.releaseDate" class="rounded-md bg-gray-100 px-3 py-1 text-sm text-gray-700">
                {{ new Date(media.releaseDate).getFullYear() }}
              </span>
              <span v-if="media.rating" class="rounded-md bg-yellow-100 px-3 py-1 text-sm font-semibold text-yellow-800">
                ⭐ {{ media.rating }}/10
              </span>
            </div>

            <p v-if="media.description" class="mb-6 text-gray-700">
              {{ media.description }}
            </p>

            <!-- Rating Section -->
            <div class="mb-6 rounded-lg bg-gray-50 p-4">
              <h3 class="mb-3 font-semibold text-gray-900">Votre note</h3>
              <div v-if="isAuthenticated">
                <div v-if="userRating" class="flex items-center gap-2">
                  <span class="text-lg font-semibold text-yellow-600">⭐ {{ userRating.score }}/10</span>
                  <span class="text-sm text-gray-600">Vous avez noté ce média</span>
                </div>
                <div v-else>
                  <div class="flex items-center gap-2">
                    <input
                      v-model.number="newRating"
                      type="number"
                      min="1"
                      max="10"
                      placeholder="1-10"
                      class="w-20 rounded-md border px-3 py-2 text-sm"
                    />
                    <button
                      @click="submitRating"
                      :disabled="isSubmittingRating"
                      class="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 disabled:opacity-50"
                    >
                      {{ isSubmittingRating ? 'Notation...' : 'Noter' }}
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="text-sm text-gray-600">
                <NuxtLink to="/users/login" class="text-blue-600 hover:text-blue-500">Connectez-vous</NuxtLink>
                pour noter ce média.
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-3">
              <NuxtLink
                to="/"
                class="inline-flex items-center rounded-md bg-gray-200 px-4 py-2 text-sm font-medium text-gray-800 transition-all duration-200 ease-out hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-1"
              >
                ← Retour
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Reviews Section -->
      <div class="rounded-xl bg-white p-6 shadow-lg sm:p-8">
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-2xl font-bold text-gray-900">Avis</h2>
          <button
            v-if="isAuthenticated && !showReviewForm"
            @click="showReviewForm = true"
            class="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1"
          >
            + Ajouter un avis
          </button>
        </div>

        <!-- Review Form -->
        <div v-if="showReviewForm" class="mb-6 rounded-lg bg-gray-50 p-4">
          <h3 class="mb-4 text-lg font-semibold text-gray-900">Rédiger un avis</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Titre</label>
              <input
                v-model="newReview.title"
                type="text"
                placeholder="Titre de votre avis"
                class="mt-1 block w-full rounded-md border px-3 py-2 text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Votre avis</label>
              <textarea
                v-model="newReview.content"
                rows="4"
                placeholder="Partagez votre opinion..."
                class="mt-1 block w-full rounded-md border px-3 py-2 text-sm"
              ></textarea>
            </div>
            <div class="flex items-center gap-2">
              <input
                v-model="newReview.spoiler"
                type="checkbox"
                id="spoiler"
                class="h-4 w-4 rounded border-gray-300"
              />
              <label for="spoiler" class="text-sm text-gray-700">Contient des spoilers</label>
            </div>
            <div v-if="reviewError" class="rounded-md bg-red-50 p-3">
              <p class="text-sm text-red-800">{{ reviewError }}</p>
            </div>
            <div class="flex gap-2">
              <button
                @click="submitReview"
                :disabled="isSubmittingReview"
                class="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 disabled:opacity-50"
              >
                {{ isSubmittingReview ? 'Publication...' : 'Publier' }}
              </button>
              <button
                @click="showReviewForm = false"
                class="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition-all duration-200 ease-out hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-1"
              >
                Annuler
              </button>
            </div>
          </div>
        </div>

        <!-- Reviews List -->
        <div v-if="reviews.length > 0" class="space-y-4">
          <div
            v-for="review in reviews"
            :key="review.id"
            class="rounded-lg border border-gray-200 bg-gray-50 p-4"
          >
            <div class="mb-2 flex items-center justify-between">
              <h4 class="font-semibold text-gray-900">{{ review.title }}</h4>
              <span class="text-sm text-gray-500">{{ formattedDate(review.created_at) }}</span>
            </div>
            <p class="text-gray-700">{{ review.content }}</p>
            <div class="mt-2 flex items-center gap-2">
              <span v-if="review.user" class="text-sm font-medium text-gray-600">
                {{ review.user.username }}
              </span>
              <span v-if="review.spoiler" class="rounded-md bg-yellow-100 px-2 py-0.5 text-xs font-semibold text-yellow-800">
                ⚠️ Spoiler
              </span>
              <span v-if="review.like_count > 0" class="text-sm text-gray-500">
                ❤️ {{ review.like_count }}
              </span>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8 text-gray-500">
          Aucun avis pour ce média. Soyez le premier à donner votre avis !
        </div>
      </div>
    </div>
  </div>
</template>