<script setup lang="ts">
  const route = useRoute()

  const hiddenRoutes = ['/users/login', '/inscription', "/users/new"]

  const showSearch = computed(() => {
    return !hiddenRoutes.includes(route.path) && !route.path.startsWith('/users/')
  })
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <LayoutAppNav />

    <div v-if="showSearch" class="search-fixed" role="search" style="position:fixed;top:70px;left:0;right:0;display:block;z-index:45;padding:16px 40px 0;pointer-events:none;box-sizing:border-box;display: flex; align-items: center; justify-content: center;">
      <div class="search-inner" style="width:50%;box-sizing:border-box;pointer-events:auto;">
        <input type="search" placeholder="Rechercher..." aria-label="Rechercher" style="width:100%;height:40px;border-radius:999px;padding:0 24px;background:rgba(43,34,98,0.96);border:0.5px solid #3f3790;color:#CFC9F4;font-size:15px;box-shadow:0 0 0 1px rgba(101,88,198,0.18) inset, 0 0 0 1px rgba(38,33,92,0.35);box-sizing:border-box;" />
      </div>
    </div>
    
    <div class="w-full px-0 py-0 flex-grow flex flex-col md:flex-row gap-8">
      <!-- Main Content -->
      <main class="w-full">
        <slot />
      </main>
    </div>
    <LayoutAppFooter />
  </div>
</template>