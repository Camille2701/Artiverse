<script setup lang="ts">
definePageMeta({
  middleware: 'guest'
})
</script>

<template>
    <div class="mx-auto w-full max-w-md space-y-6 px-4 py-8 sm:space-y-8 sm:px-6 sm:py-12 lg:max-w-lg lg:px-0">
        <div class="text-center">
            <h1 class="text-3xl sm:text-4xl font-display font-bold text-text-primary mb-2">
                Bienvenue
            </h1>
            <p class="text-text-secondary font-body">Connecte-toi pour accéder à ton espace</p>
        </div>
        <UserLogin />
        <p class="text-center text-text-secondary font-body text-sm sm:text-base">
            Pas encore de compte ?
            <NuxtLink to="/users/new" class="text-accent hover:text-accent-hover font-semibold transition-colors underline underline-offset-4 decoration-2">
                S'inscrire
            </NuxtLink>
        </p>
    </div>
</template>