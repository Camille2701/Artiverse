<template>
  <article class="media-card" :aria-label="`${item.title} — ${typeLabel} — Note ${item.score}`">
    <div class="card-thumb" :style="{ background: style.bg }">
      <span class="card-rank" aria-hidden="true">N°{{ item.rank }}</span>
      <i :class="['ti', style.icon]" :style="{ color: style.color }" aria-hidden="true" />
    </div>

    <div class="card-body">
      <h3 class="card-title">{{ item.title }}</h3>
      <p class="card-meta">{{ item.year }} · {{ typeLabel }}</p>

      <div class="card-rating">
        <span class="card-stars" aria-hidden="true">{{ stars }}</span>
        <span class="card-score">{{ item.score }}</span>
      </div>

      <ul v-if="item.tags.length" class="card-tags" role="list">
        <li v-for="(tag, i) in item.tags" :key="tag" :class="['tag', i === 0 ? style.tagClass : '']">
          {{ tag }}
        </li>
      </ul>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { MediaItem } from '~/types'

const props = defineProps<{ item: MediaItem }>()

const { getStyle, starsFromScore } = useMediaStyle()

const style   = computed(() => getStyle(props.item.type))
const stars   = computed(() => starsFromScore(props.item.score))
const typeLabel = computed(() => style.value.label)
</script>

<style scoped>
/* styling provided by global artiverse CSS */
</style>
