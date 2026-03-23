<template>

    <div class="p-6 mb-4 bg-white rounded-lg shadow-md">
        <h1 class="text-xl text-gray-900">{{ props.media.title }}</h1>
        <p class="text-gray-600">{{ props.media.description }}</p>
        <p class="text-lg font-bold text-blue-500">Note: {{ props.media.rating }}/10</p>

        <!-- <img src="{{ props.media.image }}" alt="{{ props.media.title }}"> -->
    </div>




</template>



<script setup lang="ts">
import type { Media } from '~~/types/media';

const props = defineProps<{
  media: Media
}>();
</script>