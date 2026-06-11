<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSocial } from '~/composables/useSocial'
import type { ActivityLog } from '~/types/user'

const { getActivityFeed } = useSocial()

const activities = ref<ActivityLog[]>([])
const isLoading = ref(false)
const currentPage = ref(0)
const totalPages = ref(0)

const { user: currentUser } = useAuth()

onMounted(async () => {
  await loadActivities()
})

async function loadActivities() {
  try {
    isLoading.value = true
    const result = await getActivityFeed({ skip: currentPage.value * 10, limit: 10 })
    activities.value = result.items
    totalPages.value = Math.ceil(result.total / 10)
  } catch (error: any) {
    console.error('Failed to load activity feed:', error)
  } finally {
    isLoading.value = false
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value - 1) {
    currentPage.value++
    loadActivities()
  }
}

function prevPage() {
  if (currentPage.value > 0) {
    currentPage.value--
    loadActivities()
  }
}

const getActivityIcon = (activityType: string) => {
  const icons: Record<string, string> = {
    'review_created': '✍️',
    'rating_given': '⭐',
    'list_created': '📋',
    'media_added_to_list': '➕',
    'badge_earned': '🏆',
    'level_up': '🎖️'
  }
  return icons[activityType] || '📌'
}

const getActivityText = (activity: ActivityLog) => {
  const username = currentUser.value?.username || 'Someone'
  switch (activity.activity_type) {
    case 'review_created':
      return `${username} wrote a review`
    case 'rating_given':
      return `${username} rated something`
    case 'list_created':
      return `${username} created a list`
    case 'media_added_to_list':
      return `${username} added media to a list`
    case 'badge_earned':
      return `${username} earned a badge!`
    case 'level_up':
      return `${username} leveled up!`
    default:
      return `${username} performed an action`
  }
}

const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now.getTime() - date.getTime()) / 1000)

  if (diff < 60) return 'Just now'
  if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`
  if (diff < 604800) return `${Math.floor(diff / 86400)} days ago`
  return date.toLocaleDateString()
}
</script>

<template>
  <div class="activity-feed max-w-2xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-6">Activity Feed</h1>

    <div v-if="isLoading" class="text-center py-8">
      <p class="text-gray-500">Loading activities...</p>
    </div>

    <div v-else-if="activities.length > 0" class="space-y-4">
      <div
        v-for="activity in activities"
        :key="activity.id"
        class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex items-start space-x-4"
      >
        <div class="text-2xl">{{ getActivityIcon(activity.activity_type) }}</div>
        <div class="flex-1">
          <p class="text-gray-800 dark:text-gray-200">{{ getActivityText(activity) }}</p>
          <p class="text-sm text-gray-500 mt-1">{{ formatTime(activity.created_at) }}</p>
          <div v-if="activity.activity_metadata" class="mt-2 text-sm text-gray-600">
            <pre>{{ JSON.stringify(activity.activity_metadata, null, 2) }}</pre>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-8">
      <p class="text-gray-500">No recent activity</p>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex justify-between items-center mt-6">
      <button
        @click="prevPage"
        :disabled="currentPage === 0"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        Previous
      </button>
      <span class="text-gray-600">Page {{ currentPage + 1 }} of {{ totalPages }}</span>
      <button
        @click="nextPage"
        :disabled="currentPage >= totalPages - 1"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        Next
      </button>
    </div>
  </div>
</template>