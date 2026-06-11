<template>
  <section class="catalog-page">
    <div class="catalog-hero">
      <div class="catalog-hero__copy">
        <span class="catalog-pill">
          <span class="catalog-pill__dot" aria-hidden="true" />
          {{ eyebrow }}
        </span>

        <h1 class="catalog-title">{{ title }}</h1>
        <p class="catalog-text">{{ description }}</p>

        <div class="catalog-stats" role="list" aria-label="Statistiques du catalogue">
          <div class="catalog-stat" role="listitem">
            <span class="catalog-stat__value">{{ items.length }}</span>
            <span class="catalog-stat__label">Titres</span>
          </div>
          <div class="catalog-stat" role="listitem">
            <span class="catalog-stat__value">{{ averageScore }}</span>
            <span class="catalog-stat__label">Note moyenne</span>
          </div>
          <div class="catalog-stat" role="listitem">
            <span class="catalog-stat__value">{{ latestYear }}</span>
            <span class="catalog-stat__label">Dernière sortie</span>
          </div>
        </div>
      </div>

      <div class="catalog-hero__panel">
        <div class="catalog-panel">
          <span class="catalog-panel__eyebrow">Sélection du moment</span>
          <h2 class="catalog-panel__title">{{ spotlight?.title }}</h2>
          <p class="catalog-panel__meta">{{ spotlight?.year }} · {{ spotlightLabel }}</p>
          <p class="catalog-panel__desc">{{ spotlight?.description || 'Ce titre fait partie des incontournables du catalogue.' }}</p>
        </div>
      </div>
    </div>

    <div class="catalog-grid">
      <MediaCatalogCard v-for="item in items" :key="item.id" :item="item" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { MediaItem } from '~/types'

const props = defineProps<{
  title: string
  eyebrow: string
  description: string
  items: MediaItem[]
}>()

const { getStyle } = useMediaStyle()

const spotlight = computed(() => props.items[0])
const spotlightLabel = computed(() => spotlight.value ? getStyle(spotlight.value.type).label : 'Artiverse')

const averageScore = computed(() => {
  if (!props.items.length) return '0.0'
  const total = props.items.reduce((sum, item) => sum + item.score, 0)
  return (total / props.items.length).toFixed(1)
})

const latestYear = computed(() => {
  if (!props.items.length) return '—'
  return Math.max(...props.items.map(item => item.year))
})
</script>

<style scoped>
.catalog-page{padding:42px 40px 56px;background:var(--c-void);color:var(--c-text)}
.catalog-hero{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(320px,.8fr);gap:24px;align-items:stretch;margin-bottom:28px}
.catalog-hero__copy,.catalog-panel{border:0.5px solid var(--c-border);border-radius:24px;background:linear-gradient(180deg, rgba(38,33,92,0.95) 0%, rgba(26,16,64,0.96) 100%);box-shadow:0 18px 42px rgba(0,0,0,.2)}
.catalog-hero__copy{padding:28px}
.catalog-pill{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:9999px;border:0.5px solid var(--c-gold);background:rgba(99,56,6,.22);color:var(--c-gold-light);font-size:.95rem;margin-bottom:18px}
.catalog-pill__dot{width:8px;height:8px;border-radius:9999px;background:var(--c-teal)}
.catalog-title{font-family:var(--font-display);font-size:clamp(2.4rem,5vw,4.8rem);line-height:1.02;margin-bottom:14px}
.catalog-text{max-width:58rem;color:var(--c-text-muted);font-size:1.05rem;line-height:1.7}
.catalog-stats{display:flex;flex-wrap:wrap;gap:14px;margin-top:28px}
.catalog-stat{min-width:160px;padding:16px 18px;border-radius:18px;background:rgba(26,16,64,.75);border:0.5px solid var(--c-border-dim)}
.catalog-stat__value{display:block;font-family:var(--font-display);font-size:1.8rem;color:var(--c-gold-light)}
.catalog-stat__label{color:var(--c-text-hint);font-size:.92rem}
.catalog-hero__panel{display:flex}
.catalog-panel{width:100%;padding:24px;display:flex;flex-direction:column;justify-content:flex-end;min-height:100%}
.catalog-panel__eyebrow{color:var(--c-text-hint);text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;margin-bottom:10px}
.catalog-panel__title{font-family:var(--font-display);font-size:2rem;line-height:1.1;margin-bottom:8px}
.catalog-panel__meta{color:var(--c-gold-light);margin-bottom:14px}
.catalog-panel__desc{color:var(--c-text-muted);line-height:1.65}
.catalog-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}
@media (max-width:1100px){.catalog-hero{grid-template-columns:1fr}.catalog-grid{grid-template-columns:1fr}}
@media (max-width:700px){.catalog-page{padding:28px 18px 40px}.catalog-hero__copy,.catalog-panel{padding:20px}.catalog-grid{gap:16px}}
</style>