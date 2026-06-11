<script setup lang="ts">
import { useAuth } from '~/composables/useAuth'

const { isAuthenticated, user: currentUser } = useAuth()

// Simple admin check (in production, use proper role-based access)
const isAdmin = computed(() => {
  return isAuthenticated.value && currentUser.value?.email?.includes('admin')
})

// Redirect if not admin
if (!isAdmin.value) {
  await navigateTo('/')
}
</script>

<template>
  <div class="admin-page">
    <div v-if="isAdmin" class="admin-dashboard">
      <div class="mb-8">
        <h1 class="text-3xl font-bold">Admin Dashboard</h1>
        <p class="text-gray-600 mt-2">Manage your application content and users</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">Media Management</h3>
          <p class="text-gray-600 text-sm mb-4">Add, edit, or remove media from the platform</p>
          <NuxtLink
            to="/admin/media"
            class="inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Manage Media
          </NuxtLink>
        </div>

        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">User Management</h3>
          <p class="text-gray-600 text-sm mb-4">View and manage user accounts</p>
          <NuxtLink
            to="/admin/users"
            class="inline-block bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            Manage Users
          </NuxtLink>
        </div>

        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">Platform Statistics</h3>
          <p class="text-gray-600 text-sm mb-4">View platform-wide analytics and metrics</p>
          <NuxtLink
            to="/admin/statistics"
            class="inline-block bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600"
          >
            View Statistics
          </NuxtLink>
        </div>

        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold mb-2">Badge Management</h3>
          <p class="text-gray-600 text-sm mb-4">Manage badges and achievements</p>
          <NuxtLink
            to="/admin/badges"
            class="inline-block bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600"
          >
            Manage Badges
          </NuxtLink>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold mb-4">Quick Overview</h3>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="text-center">
            <div class="text-2xl font-bold text-blue-500">Active Users</div>
            <div class="text-sm text-gray-600">Loading...</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-green-500">Media Items</div>
            <div class="text-sm text-gray-600">Loading...</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-purple-500">Reviews</div>
            <div class="text-sm text-gray-600">Loading...</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-yellow-500">Lists</div>
            <div class="text-sm text-gray-600">Loading...</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>