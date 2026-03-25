<script setup lang="ts">
useHead({
  title: "Artiverse",
  meta: [
    { name: "Page de création d'utilisateur", content: "Création d'un utilisateur"}
  ]
})
</script>

<template>
  <div class="mx-auto w-full max-w-md space-y-4 px-4 py-6 sm:space-y-5 sm:px-6 sm:py-8 lg:max-w-lg lg:space-y-6 lg:px-0">
    <h1 class="text-2xl font-semibold text-slate-900 sm:text-3xl">M'inscrire</h1>
    <UserForm />
    <p class="text-sm text-slate-600 sm:text-base">
      Déjà un compte ?
      <NuxtLink to="/users/login" class="text-link-accent">Se connecter</NuxtLink>
    </p>
  </div>
</template>