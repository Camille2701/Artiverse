<script setup lang="ts">
useHead({
  title: 'Inscription | Artiverse',
  meta: [
    { name: 'description', content: 'Crée ton compte Artiverse pour commencer à explorer, noter et suivre tes médias favoris.' }
  ]
})
</script>

<template>
  <AuthPageShell
    eyebrow="Créer un compte"
    title="Entre dans Artiverse en quelques secondes."
    description="Crée ton espace personnel pour suivre tes coups de cœur, publier ton activité et garder ta culture au même endroit."
    :bullets="[
      'Un profil prêt à l’emploi en quelques étapes.',
      'Une interface claire pour suivre tes médias et tes envies.',
      'Le même univers visuel que le reste du site, sans rupture.'
    ]"
  >
    <div class="auth-form-stack">
      <div class="auth-heading">
        <span class="auth-kicker">Commencer maintenant</span>
        <h2>M'inscrire</h2>
        <p>Renseigne les informations demandées pour créer ton compte Artiverse.</p>
      </div>

      <UserForm />

      <p class="auth-switch">
        Déjà un compte ?
        <NuxtLink to="/users/login">Se connecter</NuxtLink>
      </p>
    </div>
  </AuthPageShell>
</template>

<style scoped>
.auth-form-stack {
  display: grid;
  gap: 22px;
}

.auth-heading {
  display: grid;
  gap: 8px;
}

.auth-kicker {
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--c-gold-light);
}

.auth-heading h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3vw, 2.4rem);
  line-height: 1.05;
  color: var(--c-text);
}

.auth-heading p {
  margin: 0;
  line-height: 1.65;
  color: var(--c-purple-muted);
}

.auth-switch {
  margin: 0;
  color: var(--c-purple-pale);
}

.auth-switch :deep(a) {
  color: var(--c-gold-light);
  font-weight: 700;
  text-decoration: none;
}

.auth-switch :deep(a:hover) {
  text-decoration: underline;
}
</style>