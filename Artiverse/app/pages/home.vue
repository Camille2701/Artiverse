<template>
    <div>
        <h1>Bienvenue sur Artiverse</h1>

        <p>Explorez et gérez votre collection de médias préférés !</p>

        <div>
            <h2 class="text-2xl font-bold text-gray-900 mb-4">Films</h2>
            <div v-if="movies.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <MediaShow v-for="movie in movies" :key="movie.id" :media="movie" />
            </div>
            <p v-else class="text-gray-500 italic">Aucun film disponible pour le moment.</p>
        </div>

        <div>
            <h2 class="text-2xl font-bold text-gray-900">Séries</h2>
            <div v-if="series.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <MediaShow v-for="serie in series" :key="serie.id" :media="serie" />
            </div>
            <p v-else class="text-gray-500 italic">Aucune série disponible pour le moment.</p>
        </div>

        <div>
            <h2 class="text-2xl font-bold text-gray-900">Jeux Vidéo</h2>
            <div v-if="games.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <MediaShow v-for="game in games" :key="game.id" :media="game" />
            </div>
            <p v-else class="text-gray-500 italic">Aucun jeu vidéo disponible pour le moment.</p>
        </div>

        <div>
            <h2 class="text-2xl font-bold text-gray-900">Livres</h2>
            <div v-if="books.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <MediaShow v-for="book in books" :key="book.id" :media="book" />
            </div>
            <p v-else class="text-gray-500 italic">Aucun livre disponible pour le moment.</p>
        </div>

    </div>
</template>

<script setup lang="ts">
import { MediaType, type Media } from '~~/types/media';


const { data: mediaList } = await useFetch<Media[]>('/api/media');

const movies = computed(() => {
    return (mediaList.value || [])
        .filter(m => m.type === MediaType.Movie)
        .slice(0, 3);
});

const series = computed(() => {
    return (mediaList.value || [])
        .filter(m => m.type === MediaType.Serie)
        .slice(0, 3);
});

const games = computed(() => {
    return (mediaList.value || [])
        .filter(m => m.type === MediaType.Game)
        .slice(0, 3);
});

const books = computed(() => {
    return (mediaList.value || [])
        .filter(m => m.type === MediaType.Book)
        .slice(0, 3);
});
</script>