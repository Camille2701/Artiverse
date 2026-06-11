<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUsers } from '~/composables/useUsers'

const { searchUsers, deleteUser } = useUsers()

const users = ref([])
const searchQuery = ref('')
const isLoading = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

onMounted(async () => {
  await loadUsers()
})

async function loadUsers() {
  try {
    isLoading.value = true
    const result = await searchUsers('', { limit: 50 })
    users.value = result.items
  } catch (error: any) {
    message.value = 'Failed to load users'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleSearch() {
  try {
    isLoading.value = true
    const result = await searchUsers(searchQuery.value, { limit: 50 })
    users.value = result.items
  } catch (error: any) {
    message.value = 'Search failed'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleDeleteUser(userId: string) {
  if (!confirm('Are you sure you want to delete this user?')) return
  try {
    isLoading.value = true
    await deleteUser(userId)
    message.value = 'User deleted successfully'
    messageType.value = 'success'
    await loadUsers()
  } catch (error: any) {
    message.value = error.message || 'Failed to delete user'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="admin-users max-w-6xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-6">User Management</h1>

    <!-- Alert Message -->
    <div
      v-if="message"
      :class="[
        'p-4 rounded mb-6',
        messageType === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
      ]"
    >
      {{ message }}
    </div>

    <!-- Search -->
    <div class="mb-6 flex gap-4">
      <input
        v-model="searchQuery"
        @keyup.enter="handleSearch"
        type="text"
        placeholder="Search users..."
        class="flex-1 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        @click="handleSearch"
        :disabled="isLoading"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
      >
        Search
      </button>
    </div>

    <!-- Users Table -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-900">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">User</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Level</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">XP</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="user in users" :key="user.id">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <img
                  v-if="user.avatar_url"
                  :src="user.avatar_url"
                  :alt="user.username"
                  class="h-8 w-8 rounded-full object-cover mr-3"
                />
                <div>
                  <div class="text-sm font-medium">{{ user.username }}</div>
                  <div class="text-sm text-gray-500">{{ user.bio || 'No bio' }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">{{ user.email }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">{{ user.level }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">{{ user.experience_points }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <NuxtLink
                :to="`/users/${user.id}`"
                class="text-blue-600 hover:text-blue-900 mr-3"
              >
                View
              </NuxtLink>
              <button
                @click="handleDeleteUser(user.id)"
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>