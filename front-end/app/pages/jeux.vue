<template>
  <MediaCatalogPage
    title="Catalogue des jeux"
    eyebrow="Gaming"
    description="Explore les jeux suivis sur Artiverse, du plus nerveux au plus ambitieux, avec un accès rapide à la fiche complète."
    :items="Games"
  />
</template>

<script setup lang="ts">
const { Games } = useGameData()

useSeoMeta({
  title: 'Artiverse — Jeux',
  description: 'Catalogue des jeux Artiverse.',
})
</script>
