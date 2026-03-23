<template>
  <div class="flex flex-col min-h-screen bg-gray-100">
    <header class="bg-indigo-600 text-white shadow-md">
      <nav class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold tracking-tight">Artiverse</h1>
        <div class="space-x-4">
          <NuxtLink to="/" class="hover:text-indigo-200 transition">manage</NuxtLink>

        </div>
      </nav>
    </header>
    
    <main class="flex-grow container mx-auto px-4 py-8">
      <slot />
    </main>
    
    <footer class="bg-gray-800 text-white py-6 text-center text-sm">
      <p>&copy; {{ new Date().getFullYear() }} Artiverse. All rights reserved.</p>
    </footer>
  </div>
</template>
