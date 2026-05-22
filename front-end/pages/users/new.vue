<script setup lang="ts">
useHead({
  title: "Artiverse - Inscription",
  meta: [
    { name: "Page de création d'utilisateur", content: "Création d'un utilisateur"}
  ]
})
</script>

<template>
  <div class="mx-auto w-full max-w-md space-y-6 px-4 py-8 sm:space-y-8 sm:px-6 sm:py-12 lg:max-w-lg lg:px-0">
    <div class="text-center">
      <h1 class="text-3xl sm:text-4xl font-display font-bold text-text-primary mb-2">
        Rejoins Artiverse
      </h1>
      <p class="text-text-secondary font-body">Crée ton compte et commence à explorer</p>
    </div>
    <UserForm />
    <p class="text-center text-text-secondary font-body text-sm sm:text-base">
      Déjà un compte ?
      <NuxtLink to="/users/login" class="text-accent hover:text-accent-hover font-semibold transition-colors underline underline-offset-4 decoration-2">
        Se connecter
      </NuxtLink>
    </p>
  </div>
</template>