<template>
    <div>
        <div class="mb-8 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
            <div>
                <h1 class="text-3xl font-extrabold text-gray-900 dark:text-text-primary">Bienvenue sur Artiverse</h1>
                <p class="mt-1 text-sm text-gray-600 dark:text-text-secondary">Explorez et gérez votre collection de médias préférés.</p>
            </div>
        </div>

        <div class="mb-8 flex flex-wrap gap-2">
            <button
                v-for="category in categories"
                :key="category.value"
                type="button"
                class="category-filter-btn"
                :class="{ 'category-filter-btn--active': selectedCategory === category.value }"
                @click="selectedCategory = category.value"
            >
                {{ category.label }}
            </button>
        </div>

        <div class="space-y-6">
            <div v-if="pending" class="flex items-center justify-center py-20">
                <div class="h-12 w-12 animate-spin rounded-full border-b-2 border-accent"></div>
                <p class="ml-3 text-gray-600 dark:text-text-secondary">Chargement des médias...</p>
            </div>

            <div v-else-if="error" class="rounded-md bg-red-50 p-6 dark:bg-red-900/20 dark:border dark:border-red-800">
                <div class="flex items-start gap-4">
                    <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/40">
                        <span class="text-red-600 dark:text-red-400">⚠️</span>
                    </div>
                    <div class="flex-1">
                        <h3 class="text-lg font-medium text-red-800 dark:text-red-400">Erreur de chargement</h3>
                        <p class="mt-2 text-sm text-red-700 dark:text-red-300">{{ getErrorMessage(error) }}</p>
                        <button
                            @click="refresh()"
                            class="mt-4 inline-flex items-center rounded-md border border-red-600 bg-transparent px-4 py-2 text-sm font-medium text-red-600 transition-all duration-200 ease-out hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1 dark:border-red-800 dark:text-red-400 dark:hover:bg-red-900/20 dark:focus:ring-red-600 dark:focus:ring-offset-bg-secondary"
                        >
                            Réessayer
                        </button>
                    </div>
                </div>
            </div>

            <div v-else>
                <div class="mb-4 flex items-center justify-between">
                    <h3 class="text-2xl font-bold text-gray-900 dark:text-text-primary">{{ selectedCategoryLabel }}</h3>
                    <span class="text-sm text-gray-500 dark:text-text-secondary">{{ filteredMedia.length }} média(s)</span>
                </div>

                <div v-if="filteredMedia.length > 0" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3">
                    <MediaShow v-for="media in filteredMedia" :key="media.id" :media="media" />
        </div>
                <div v-else class="rounded-md bg-gray-50 p-8 text-center dark:bg-bg-secondary dark:border dark:border-border-color">
                    <p class="italic text-gray-500 dark:text-text-secondary">Aucun média disponible dans cette catégorie pour le moment.</p>
                </div>
            </div>
    </div>
    </div>
</template>

<script setup lang="ts">
import { MediaType, type Media } from '~/types/media';
import { useApi } from '~/composables/useApi';

const { getErrorMessage } = useApi()
const { data: mediaList, pending, error, refresh } = await useFetch<Media[]>('/api/media');

type CategoryValue = 'all' | MediaType

const categories: Array<{ label: string; value: CategoryValue }> = [
    { label: 'Tous', value: 'all' },
    { label: 'Films', value: MediaType.Movie },
    { label: 'Séries', value: MediaType.Serie },
    { label: 'Jeux vidéo', value: MediaType.Game },
    { label: 'Livres', value: MediaType.Book }
]

const selectedCategory = ref<CategoryValue>('all')

const filteredMedia = computed(() => {
    const allMedia = mediaList.value || []
    if (selectedCategory.value === 'all') {
        return allMedia
    }

    return allMedia.filter(media => media.type === selectedCategory.value || media.type === (selectedCategory.value as string))
})

const selectedCategoryLabel = computed(() => {
    return categories.find(category => category.value === selectedCategory.value)?.label || 'Tous'
})
</script>