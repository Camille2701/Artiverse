<script setup lang="ts">
import { useAuth } from '~/composables/useAuth'

const { isAuthenticated, user: currentUser } = useAuth()
const isAdmin = computed(() => {
  return isAuthenticated.value && currentUser.value?.email?.includes('admin')
})

if (!isAdmin.value) {
  await navigateTo('/')
}
</script>

<template>
  <div class="admin-media-page">
    <MediaAdmin />
  </div>
</template>