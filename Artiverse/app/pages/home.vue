<template>
    <div>
        <h1>Bienvenue sur Artiverse</h1>

        <p>Explorez et gérez votre collection de médias préférés !</p>

        <div>
            <h2 class="text-2xl font-bold text-gray-900">Films</h2>
            
        </div>

        <div>
            <h2 class="text-2xl font-bold text-gray-900">Séries</h2>
        </div>

        <div>
            <h2 class="text-2xl font-bold text-gray-900">Jeux Vidéo</h2>
        </div>

    </div>
</template>

<script setup lang="ts">
import type { Media } from '~~/types/media';

definePageMeta({
  layout: 'content'
});

</script>