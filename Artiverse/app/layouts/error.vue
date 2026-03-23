<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 text-gray-800 p-4">
    <div class="max-w-md w-full bg-white shadow-xl rounded-lg p-8 text-center">
      <h1 class="text-4xl font-extrabold text-red-500 mb-4">Oups!</h1>
      <p class="text-lg text-gray-600 mb-6">Quelque chose s'est mal passé.</p>
      <slot />
      <div class="mt-6">
        <NuxtLink to="/" class="inline-block px-6 py-2 bg-indigo-600 text-white font-medium rounded hover:bg-indigo-700 transition">
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
