<template>
  <section class="w-full relative overflow-hidden py-12 px-6 md:px-12">
    <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
      <!-- Left: Intro -->
      <div class="lg:col-span-2">
        <span class="inline-block mb-4 px-3 py-1 rounded-full text-xs font-semibold">Rejoins 2.4 millions de passionnés</span>
        <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-white leading-tight">Ton univers culturel, <span class="text-gradient">centralisé.</span></h1>
        <p class="mt-4 text-lg text-indigo-100 max-w-2xl">Films, séries, jeux vidéo, livres — une seule plateforme pour tout noter, archiver et partager avec une communauté qui vit pour la culture.</p>

        <div class="mt-6 flex flex-col sm:flex-row gap-3">
          <button class="btn-primary px-6 py-3 rounded-md font-semibold">Commencer gratuitement</button>
          <button class="btn-secondary px-6 py-3 rounded-md">Voir la démo</button>
        </div>

        <div class="mt-8 flex gap-8 text-sm text-indigo-200">
          <div>
            <div class="text-2xl font-bold text-white">18M</div>
            <div class="text-xs">Œuvres cataloguées</div>
          </div>
          <div>
            <div class="text-2xl font-bold text-white">7,2M</div>
            <div class="text-xs">Critiques publiées</div>
          </div>
          <div>
            <div class="text-2xl font-bold text-white">430K</div>
            <div class="text-xs">Badges débloqués</div>
          </div>
        </div>
      </div>

      <!-- Right: Card preview -->
      <aside class="lg:col-span-1">
        <div class="bg-gradient-to-br from-indigo-900/60 via-purple-900/60 to-transparent border border-white/5 rounded-xl p-6 text-indigo-50">
          <div class="flex items-start justify-between">
            <span class="bg-amber-400 text-black px-3 py-1 rounded-full text-xs font-semibold">Tendance</span>
            <div class="text-sm font-semibold bg-white/5 px-2 py-1 rounded">9.4</div>
          </div>

          <div class="mt-4">
            <div class="h-28 w-full bg-white/5 rounded mb-4">
            </div>
            <h3 class="text-lg font-bold">Dune: Part Two</h3>
            <img src="/images/dune.png" alt="Dune Cover"">
            <p class="text-xs text-indigo-200 mt-1">Denis Villeneuve • 2024 • 2h48</p>
            <p class="text-sm text-indigo-200 mt-3 line-clamp-3">La suite épique de l'adaptation de Frank Herbert. Paul Atreides s'engage dans un voyage spirituel et stratégique pour devenir le Messie des Fremens.</p>
          </div>

          <div class="mt-4 flex gap-2">
            <div class="text-xs bg-white/5 px-3 py-1 rounded">Science-fiction</div>
            <div class="text-xs bg-white/5 px-3 py-1 rounded">Adapté du roman</div>
          </div>
        </div>
      </aside>
    </div>
  </section>
</template>

<script setup lang="ts">
</script>

<style scoped>
.text-gradient {
  background: linear-gradient(90deg,#ffb86b,#7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.btn-primary {
  background: linear-gradient(90deg,#7c3aed,#5b21b6);
  color: white;
}
.btn-secondary {
  background: rgba(255,255,255,0.06);
  color: #e6e6ff;
  border: 1px solid rgba(255,255,255,0.04);
}
</style>
