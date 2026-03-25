<template>
    <div>
        <div class="mb-8 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
            <div>
                <h1 class="text-3xl font-extrabold text-gray-900">Bienvenue sur Artiverse</h1>
                <p class="mt-1 text-sm text-gray-600">Explorez et gérez votre collection de médias préférés.</p>
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
            </div>

            <div v-else-if="error" class="rounded-md bg-red-50 p-4">
                <h3 class="text-lg font-medium text-red-800">Erreur</h3>
                <p class="mt-2 text-sm text-red-700">{{ error.message }}</p>
                <button @click="refresh()" class="mt-4 text-sm font-medium text-red-600 hover:text-red-500">Réessayer</button>
            </div>

            <div v-else>
                <h3 class="mb-4 text-2xl font-bold text-gray-900">{{ selectedCategoryLabel }}</h3>
                <div v-if="filteredMedia.length > 0" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3">
                    <MediaShow v-for="media in filteredMedia" :key="media.id" :media="media" />
        </div>
                <p v-else class="italic text-gray-500">Aucun média disponible dans cette catégorie pour le moment.</p>
            </div>
    </div>
    </div>
</template>

<script setup lang="ts">
import { MediaType, type Media } from '~~/types/media';

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

    return allMedia.filter(media => media.type === selectedCategory.value)
})

const selectedCategoryLabel = computed(() => {
    return categories.find(category => category.value === selectedCategory.value)?.label || 'Tous'
})
</script>