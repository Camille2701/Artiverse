<template>
  <div class="page">
    <main id="main-content">

      <!-- Hero -->
      <HomeHeroSection
        :stats="stats"
        :featured="featuredItem"
        :side-items="sideItems"
      />

      <div class="section-separator" role="separator" />

      <div class="content-frame" style="padding:0 40px;box-sizing:border-box;">
        <!-- Trending -->
        <HomeTrendingSection :items="trending" />

        <div class="section-separator" role="separator" />

        <!-- Activity + Categories -->
        <section class="two-col" aria-label="Communauté et exploration">
          <HomeActivityFeed :items="activity" />
          <HomeCategoryGrid :categories="categories" />
        </section>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
const { stats, featuredItem, sideItems, trending, activity, categories } = useHomeData()

useSeoMeta({
  title: 'Artiverse — Ton univers culturel centralisé',
  description: 'Note, catalogue et partage tes films, séries, jeux et livres. Rejoins une communauté de passionnés.',
  ogTitle: 'Artiverse',
  ogDescription: 'Films, séries, jeux vidéo, livres — une seule plateforme.',
})
</script>

<style scoped>
.page { min-height: 100vh; background: var(--c-void); }
.bottom-grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; padding:28px 40px 48px; }
@media (max-width:700px){ .bottom-grid{grid-template-columns:1fr;padding:24px 20px 40px;} }
</style>
