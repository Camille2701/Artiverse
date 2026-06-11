<script setup lang="ts">
const { isAuthenticated, restoreSession, user: currentUser } = useAuth()
const route = useRoute()

if (!isAuthenticated.value) {
  await restoreSession()
}

if (!isAuthenticated.value) {
  await navigateTo('/users/login')
}

const isOwnSettings = computed(() =>
  String(currentUser.value?.id) === String(route.params.id)
)
</script>

<template>
  <div class="settings-page">
    <UserSettings v-if="isOwnSettings" />
    <div v-else class="max-w-2xl mx-auto p-6">
      <h1 class="text-2xl font-bold mb-4">Access Denied</h1>
      <p class="text-gray-600">You can only access your own settings.</p>
    </div>
  </div>
</template>