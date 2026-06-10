<template>
  <section class="sec" aria-labelledby="trending-title">
    <div class="sec-head">
      <div class="sec-title-group">
        <h2 id="trending-title" class="sec-title">TENDANCES</h2>
        <!-- <span class="sec-sub" aria-hidden="true">cette semaine</span> -->
      </div>
      <NuxtLink to="/tendances" class="sec-more">
        Tout voir
        <i class="ti ti-arrow-right" aria-hidden="true" />
      </NuxtLink>
    </div>

    <ul class="cards-grid" role="list">
      <li v-for="item in items" :key="item.id">
        <UiMediaCard :item="item" />
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { MediaItem } from '~/types'

defineProps<{ items: MediaItem[] }>()
</script>

<style scoped>
/* visual rules are provided by global artiverse CSS */
</style>
