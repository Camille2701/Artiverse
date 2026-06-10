<template>
  <section class="hero" aria-label="Présentation de la plateforme">
    <!-- Ambient background -->
    <div class="hero-bg" aria-hidden="true">
      <div class="orb orb-1" />
      <div class="orb orb-2" />
      <div class="orb orb-3" />
      <div class="grid-dots" />
    </div>

    <!-- Left: copy -->
    <div class="hero-left">
      <span class="hero-pill gold">
        <span class="pulse-dot" aria-hidden="true" />
        Rejoins 2,4 millions de passionnés
      </span>

      <h1 class="hero-h1">
        Ton univers<br>
        culturel,<br>
        <em>centralisé.</em>
      </h1>

      <p class="hero-sub">
        Films, séries, jeux vidéo, livres — une seule plateforme
        pour tout noter, archiver et partager avec une communauté
        qui vit pour la culture.
      </p>

      <div class="hero-actions">
        <button class="btn-cta">Commencer gratuitement</button>
        <button class="btn-ghost">
          <i class="ti ti-player-play" aria-hidden="true" />
          Voir la démo
        </button>
      </div>
    </div>

    <!-- Right: featured card -->
    <div class="hero-right">
      <article class="feat-card">
        <div class="feat-thumb">
          <div class="feat-img-zone">
            <img class="feat-card-img" src="/images/dune.png" alt="Dune Cover"">
          </div>
          <span class="feat-badge">Tendance</span>
          <span class="feat-score" aria-label="Note : 9.4">9.4</span>
        </div>

        <div class="feat-body">
          <h2 class="feat-title">{{ featured.title }}</h2>
          <p class="feat-meta">{{ featured.director }} · {{ featured.year }} · {{ featured.duration }}</p>
          <ul class="feat-tags" role="list">
            <li v-for="tag in featured.tags" :key="tag" :class="['ftag', tagClass(tag)]">{{ tag }}</li>
          </ul>
          <p class="feat-desc">{{ featured.description }}</p>
        </div>
      </article>

      <ul class="mini-cards-row" role="list">
        <li v-for="item in sideItems" :key="item.id" class="mini-list">
            <div class="mini-card">
                <div class="mini-icon">
                    <img :src="`/images/${item.imgLink}.png`" :alt="item.imgAlt">
                </div>
                <div class="mini-info">
                    <span class="mini-title">{{ item.title }}</span>
                    <span class="mini-score" :aria-label="`Note : ${item.score}`">★ {{ item.score }}</span>
                </div>
            </div>
        </li>
      </ul>
    </div>
  </section>
    <ul class="hero-stats" role="list" aria-label="Chiffres clés">
        <li v-for="(stat, i) in stats" :key="stat.label" class="hstat">
            <div class="stats-content"><img
                :src="`/icons/${statIcons[i]}.png`"
                :alt="stat.imgAlt"
            >
            </div>
            <div>
                <span class="hstat-n">{{ stat.value }}</span><br>
                <span class="hstat-l">{{ stat.label }}</span>
            </div>
        </li>
    </ul>
</template>

<script setup lang="ts">
import type { MediaItem, StatItem, SideItem } from '~/types'

const { getStyle } = useMediaStyle()

const props = defineProps<{
  stats:     StatItem[]
  featured:  MediaItem
  sideItems: SideItem[]
}>()

const specialTags: Record<string, string> = {
  'Adapté du roman': 'ftag-g',
}
const tagClass = (tag: string) => specialTags[tag] ?? ''

const statIcons = ['oeuvres','critiques','badges','comptes']
</script>

<style scoped>
</style>
