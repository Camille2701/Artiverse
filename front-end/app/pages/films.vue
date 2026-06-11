<template>
  <MediaCatalogPage
    title="Catalogue des films"
    eyebrow="Cinéma"
    description="Retrouve ici la sélection des films Artiverse, avec leurs notes, leurs genres et un accès direct à chaque fiche média."
    :items="Movies"
  />
</template>

<script setup lang="ts">
const { Movies } = useMovieData()

useSeoMeta({
  title: 'Artiverse — Films',
  description: 'Catalogue des films Artiverse.',
})
</script>
