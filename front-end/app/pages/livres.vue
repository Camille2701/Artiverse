<template>
  <MediaCatalogPage
    title="Catalogue des livres"
    eyebrow="Littérature"
    description="Découvre les livres présents dans Artiverse, des classiques incontournables aux titres les plus récents."
    :items="Books"
  />
</template>

<script setup lang="ts">
const { Books } = useBookData()

useSeoMeta({
  title: 'Artiverse — Livres',
  description: 'Catalogue des livres Artiverse.',
})
</script>
