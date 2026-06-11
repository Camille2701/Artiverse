<script setup lang="ts">
useHead({
    title: 'Connexion | Artiverse',
    meta: [
        { name: 'description', content: 'Connecte-toi à Artiverse pour retrouver tes médias, tes notes et ton activité.' }
    ]
})
</script>

<template>
    <AuthPageShell
        eyebrow="Accès membre"
        title="Replonge dans ton univers culturel."
        description="Connecte-toi pour retrouver ta bibliothèque, tes recommandations et ton activité sur Artiverse."
        :bullets="[
            'Retrouve tes listes et tes favoris en un instant.',
            'Reprends la découverte là où tu l’avais laissée.',
            'Garde un espace fluide, sobre et rapide sur tous tes écrans.'
        ]"
    >
        <div class="auth-form-stack">
            <div class="auth-heading">
                <span class="auth-kicker">Bienvenue à nouveau</span>
                <h2>Me connecter</h2>
                <p>Entre ton email et ton mot de passe pour accéder à ton espace personnel.</p>
            </div>

            <UserLogin />

            <p class="auth-switch">
                Pas encore de compte ?
                <NuxtLink to="/users/new">S'inscrire</NuxtLink>
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