<template>
  <NuxtLink :to="`/media/${item.id}`" class="catalog-link">
    <article class="catalog-card">
      <div class="catalog-card__media">
        <img class="catalog-card__img" :src="`/images/${item.imgLink}`" :alt="item.imgAlt">
        <span class="catalog-card__score">★ {{ item.score }}</span>
      </div>

      <div class="catalog-card__body">
        <div class="catalog-card__head">
          <h3 class="catalog-card__title">{{ item.title }}</h3>
          <span class="catalog-card__type">{{ typeLabel }}</span>
        </div>

        <p class="catalog-card__meta">{{ item.year }} · {{ item.director || item.author || 'Artiverse' }}</p>

        <ul class="catalog-card__tags" role="list">
          <li v-for="tag in item.tags.slice(0, 3)" :key="tag" class="catalog-card__tag" :class="style.tagClass">
            {{ tag }}
          </li>
        </ul>

        <p class="catalog-card__description">
          {{ item.description || 'Aucune description disponible pour le moment.' }}
        </p>

        <div class="catalog-card__footer">
          <span>{{ reviewCount }} critiques</span>
          <span class="catalog-card__cta">Voir la fiche</span>
        </div>
      </div>
    </article>
  </NuxtLink>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { MediaItem } from '~/types'

const props = defineProps<{
  item: MediaItem
}>()

const { getStyle } = useMediaStyle()

const style = computed(() => getStyle(props.item.type))
const typeLabel = computed(() => style.value.label)
const reviewCount = computed(() => props.item.critiques?.length ?? 0)
</script>

<style scoped>
.catalog-link{display:block;height:100%;text-decoration:none}
.catalog-card{height:100%;overflow:hidden;border:0.5px solid var(--c-border);border-radius:20px;background:linear-gradient(180deg, rgba(38,33,92,0.98) 0%, rgba(26,16,64,0.96) 100%);transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease;box-shadow:0 12px 36px rgba(0,0,0,.18)}
.catalog-card:hover{transform:translateY(-4px);border-color:var(--c-gold);box-shadow:0 18px 45px rgba(0,0,0,.28)}
.catalog-card__media{position:relative;height:210px;background:var(--c-deep)}
.catalog-card__img{width:100%;height:100%;object-fit:cover;display:block}
.catalog-card__score{position:absolute;top:12px;right:12px;padding:4px 10px;border-radius:9999px;background:rgba(26,16,64,.82);border:0.5px solid var(--c-border);color:var(--c-gold-light);font-family:var(--font-display);font-weight:600}
.catalog-card__body{display:flex;flex-direction:column;gap:10px;padding:18px}
.catalog-card__head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}
.catalog-card__title{font-family:var(--font-display);font-size:1.2rem;line-height:1.2;color:var(--c-text)}
.catalog-card__type{flex-shrink:0;padding:4px 10px;border-radius:9999px;background:var(--c-gold-dark);color:var(--c-gold-light);font-size:.8rem}
.catalog-card__meta{color:var(--c-text-hint);font-size:.95rem}
.catalog-card__tags{display:flex;flex-wrap:wrap;gap:6px}
.catalog-card__tag{padding:3px 10px;border-radius:9999px;background:var(--c-indigo-mid);color:var(--c-purple-pale);font-size:.82rem}
.catalog-card__description{color:var(--c-text-muted);line-height:1.55;font-size:.95rem;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;min-height:4.6em}
.catalog-card__footer{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-top:10px;border-top:0.5px solid var(--c-border-faint);color:var(--c-text-hint);font-size:.9rem}
.catalog-card__cta{color:var(--c-gold-light);font-family:var(--font-display)}
</style>