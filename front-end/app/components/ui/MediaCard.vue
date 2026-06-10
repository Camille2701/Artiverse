<template>
  <article class="mcard" :aria-label="`${item.title} — ${typeLabel} — Note ${item.score}`">
    <div class="mcard-top" :style="{ background: style.bg }">
      <span class="mcard-rank" aria-hidden="true">N°{{ item.rank }}</span>
      <i class="mcard-icon" :style="{ color: style.color }" aria-hidden="true" />
    </div>

    <div class="mcard-body">
      <h3 class="mcard-title">{{ item.title }}</h3>
      <p class="mcard-meta">{{ item.year }} · {{ typeLabel }}</p>

      <div class="mcard-stars">
        <span class="card-stars" aria-hidden="true">{{ stars }}</span>
        <span class="card-score">{{ item.score }}</span>
      </div>

      <ul v-if="item.tags.length" class="mcard-tags" role="list">
        <li v-for="(tag, i) in item.tags" :key="tag" :class="['tag', i === 0 ? style.tagClass : '']" class="mtag">
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
