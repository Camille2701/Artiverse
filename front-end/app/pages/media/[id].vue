<template>
  <section v-if="media" class="media-page">
    <nav class="media-breadcrumb" aria-label="Fil d'ariane">
      <NuxtLink :to="catalogPath" class="media-breadcrumb__link">{{ catalogLabel }}</NuxtLink>
      <span aria-hidden="true">/</span>
      <span>{{ media.title }}</span>
    </nav>

    <div class="media-layout">
      <article class="media-card">
        <div class="media-card__visual">
          <img class="media-card__img" :src="`/images/${media.imgLink}`" :alt="media.imgAlt">
          <div class="media-card__badges">
            <span class="media-badge">{{ style.label }}</span>
            <span class="media-score">★ {{ media.score }}</span>
          </div>
        </div>

        <div class="media-card__body">
          <h1 class="media-title">{{ media.title }}</h1>
          <p class="media-meta">{{ media.year }} · {{ media.director || media.author || 'Artiverse' }}</p>

          <ul class="media-tags" role="list">
            <li v-for="tag in media.tags" :key="tag" class="media-tag" :class="style.tagClass">{{ tag }}</li>
          </ul>

          <p class="media-description">
            {{ media.description || 'Aucune description disponible pour ce média.' }}
          </p>

          <div class="media-actions">
            <NuxtLink :to="catalogPath" class="media-button media-button--ghost">Retour au catalogue</NuxtLink>
          </div>
        </div>
      </article>

      <aside class="media-side">
        <div class="media-panel">
          <h2 class="media-panel__title">Détails</h2>
          <dl class="media-dl">
            <div>
              <dt>Type</dt>
              <dd>{{ style.label }}</dd>
            </div>
            <div>
              <dt>Note</dt>
              <dd>{{ media.score }}/10</dd>
            </div>
            <div>
              <dt>Année</dt>
              <dd>{{ media.year }}</dd>
            </div>
            <div>
              <dt>Critiques</dt>
              <dd>{{ critiqueCount }}</dd>
            </div>
          </dl>
        </div>

        <div class="media-panel">
          <h2 class="media-panel__title">Critiques</h2>
          <ul class="review-list" role="list">
            <li v-for="review in reviews" :key="review.id" class="review-item">
              <div class="review-item__head">
                <strong>{{ review.user.username }}</strong>
                <span>{{ formatDate(review.date) }}</span>
              </div>
              <div class="review-item__note">{{ review.note ?? '—' }}/10</div>
              <p>{{ review.commentaire }}</p>
            </li>
          </ul>
        </div>
      </aside>
    </div>
  </section>

  <section v-else class="media-page media-page--empty">
    <h1>Média introuvable</h1>
    <p>Le média demandé n’existe pas dans le catalogue.</p>
    <NuxtLink to="/" class="media-button">Retour à l'accueil</NuxtLink>
  </section>
</template>

<script setup lang="ts">
const route = useRoute()
const { findMediaById } = useCatalogMedia()

const media = computed(() => findMediaById(route.params.id))
const { getStyle } = useMediaStyle()

const style = computed(() => {
  if (!media.value) {
    return getStyle('film')
  }

  return getStyle(media.value.type)
})

const catalogPath = computed(() => {
  if (!media.value) return '/'

  switch (media.value.type) {
    case 'film': return '/films'
    case 'serie': return '/series'
    case 'jeu': return '/jeux'
    case 'livre': return '/livres'
  }
})

const catalogLabel = computed(() => {
  if (!media.value) return 'Catalogue'

  return style.value.label
})

const reviews = computed(() => media.value?.critiques ?? [])
const critiqueCount = computed(() => reviews.value.length)

function formatDate(date: Date) {
  return new Date(date).toLocaleDateString('fr-FR')
}

useSeoMeta(() => ({
  title: media.value ? `Artiverse — ${media.value.title}` : 'Artiverse — Média introuvable',
  description: media.value?.description || 'Fiche détaillée d’un média Artiverse.',
}))

if (!media.value) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Média introuvable',
  })
}
</script>

<style scoped>
.media-page{padding:42px 40px 56px;background:var(--c-void);color:var(--c-text)}
.media-breadcrumb{display:flex;align-items:center;gap:10px;color:var(--c-text-hint);margin-bottom:18px;font-size:.95rem}
.media-breadcrumb__link{color:var(--c-gold-light);text-decoration:none}
.media-layout{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(300px,.75fr);gap:24px}
.media-card,.media-panel{border:0.5px solid var(--c-border);border-radius:24px;background:linear-gradient(180deg, rgba(38,33,92,0.95) 0%, rgba(26,16,64,0.96) 100%);box-shadow:0 18px 42px rgba(0,0,0,.2)}
.media-card{overflow:hidden}
.media-card__visual{position:relative;height:420px;background:var(--c-deep)}
.media-card__img{width:100%;height:100%;object-fit:cover;display:block}
.media-card__badges{position:absolute;inset:16px 16px auto;display:flex;justify-content:space-between;gap:12px}
.media-badge,.media-score{padding:6px 12px;border-radius:9999px;font-family:var(--font-display);font-weight:600}
.media-badge{background:rgba(99,56,6,.92);color:var(--c-gold-light)}
.media-score{background:rgba(26,16,64,.86);border:0.5px solid var(--c-border);color:var(--c-gold-light)}
.media-card__body{padding:26px}
.media-title{font-family:var(--font-display);font-size:clamp(2rem,4vw,3.6rem);line-height:1.05;margin-bottom:10px}
.media-meta{color:var(--c-text-hint);font-size:1rem;margin-bottom:16px}
.media-tags{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px}
.media-tag{padding:4px 12px;border-radius:9999px;background:var(--c-indigo-mid);color:var(--c-purple-pale);font-size:.88rem}
.media-description{color:var(--c-text-muted);line-height:1.8;font-size:1.02rem}
.media-actions{margin-top:24px}
.media-button{display:inline-flex;align-items:center;justify-content:center;padding:11px 18px;border-radius:12px;border:0.5px solid var(--c-gold);background:var(--c-gold-dark);color:var(--c-gold-light);text-decoration:none;font-family:var(--font-display)}
.media-button--ghost{background:transparent;border-color:var(--c-border);color:var(--c-text)}
.media-side{display:flex;flex-direction:column;gap:18px}
.media-panel{padding:22px}
.media-panel__title{font-family:var(--font-display);font-size:1.4rem;margin-bottom:16px}
.media-dl{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.media-dl div{padding:14px;border-radius:16px;background:rgba(26,16,64,.78);border:0.5px solid var(--c-border-dim)}
.media-dl dt{color:var(--c-text-hint);font-size:.85rem;margin-bottom:6px}
.media-dl dd{color:var(--c-text);font-family:var(--font-display);font-size:1.15rem}
.review-list{display:flex;flex-direction:column;gap:12px}
.review-item{padding:14px 16px;border-radius:18px;background:rgba(26,16,64,.75);border:0.5px solid var(--c-border-dim)}
.review-item__head{display:flex;justify-content:space-between;gap:12px;color:var(--c-text-muted);margin-bottom:8px}
.review-item__note{color:var(--c-gold-light);font-family:var(--font-display);margin-bottom:8px}
.media-page--empty{min-height:calc(100vh - 120px);display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:14px}
.media-page--empty h1{font-family:var(--font-display);font-size:clamp(2rem,4vw,3rem)}
@media (max-width:1100px){.media-layout{grid-template-columns:1fr}.media-card__visual{height:320px}}
@media (max-width:700px){.media-page{padding:28px 18px 40px}.media-card__body,.media-panel{padding:18px}.media-dl{grid-template-columns:1fr}.media-card__visual{height:240px}.media-breadcrumb{flex-wrap:wrap}}
</style>