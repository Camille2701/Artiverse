<template>
  <MediaCatalogPage
    title="Catalogue des séries"
    eyebrow="Séries"
    description="Retrouve les séries sélectionnées par la communauté Artiverse avec leurs notes, thèmes et fiches détaillées."
    :items="Series"
  />
</template>

<script setup lang="ts">
const { Series } = useSeriesData()

useSeoMeta({
  title: 'Artiverse — Séries',
  description: 'Catalogue des séries Artiverse.',
})
</script>
