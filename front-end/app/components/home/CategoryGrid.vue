<template>
  <section aria-labelledby="categories-title">
    <div class="sec-header">
      <h2 id="categories-title" class="sec-title">EXPLORER</h2>
    </div>

    <ul class="cat-grid" role="list">
      <li v-for="cat in categories" :key="cat.id">
        <NuxtLink :to="categoryPath(cat.id)" class="cat-item" :aria-label="`${cat.label} — ${cat.count}`">
          <div class="cat-icon-wrap" :style="{ background: cat.iconBg }">
            <i :class="['ti', cat.icon]" :style="{ color: cat.iconColor }" aria-hidden="true" />
          </div>
          <div class="cat-info">
            <span class="cat-name">{{ cat.label }}</span>
            <span class="cat-count">{{ cat.count }}</span>
          </div>
          <i class="ti ti-arrow-right cat-arr" aria-hidden="true" />
        </NuxtLink>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { CategoryItem } from '~/types'
defineProps<{ categories: CategoryItem[] }>()

const categoryPath = (id: CategoryItem['id']) => {
  switch (id) {
    case 'film': return '/films'
    case 'serie': return '/series'
    case 'jeu': return '/jeux'
    case 'livre': return '/livres'
  }
}
</script>

<style scoped>
/* visual rules provided by global CSS */
</style>
