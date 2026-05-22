<template>
  <div class="space-y-4">
    <h3 class="text-lg font-display font-semibold text-text-primary">{{ title }}</h3>

    <div v-if="badges.length === 0" class="text-center py-8">
      <p class="text-text-tertiary italic">Aucun badge débloqué pour le moment</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <Badge
        v-for="badge in badges"
        :key="badge.id"
        :badge="badge"
        :size="size"
        class="cursor-pointer hover:scale-105 transition-transform"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import Badge from './Badge.vue'

interface Badge {
  id: string
  name: string
  description?: string
  icon?: string
  level?: string
  style: 'flat' | 'gradient' | 'glass' | 'holographic'
  mediaType?: 'movie' | 'series' | 'game' | 'book'
}

interface Props {
  title?: string
  badges: Badge[]
  size?: 'sm' | 'md' | 'lg'
}

withDefaults(defineProps<Props>(), {
  title: 'Badges',
  size: 'md'
})
</script>