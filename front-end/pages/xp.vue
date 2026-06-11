<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useXP } from '~/composables/useXP'
import type { XPProgress, LeaderboardEntry } from '~/types/xp'

const { getXPProgress, getLeaderboard, claimDailyLogin } = useXP()

const xpProgress = ref<XPProgress | null>(null)
const leaderboard = ref<LeaderboardEntry[]>([])
const isLoading = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

onMounted(async () => {
  await loadData()
})

async function loadData() {
  try {
    isLoading.value = true
    xpProgress.value = await getXPProgress()
    leaderboard.value = await getLeaderboard({ limit: 10 })
  } catch (error: any) {
    message.value = 'Failed to load XP data'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleClaimDaily() {
  try {
    isLoading.value = true
    const result = await claimDailyLogin()
    message.value = `Claimed ${result.xp_gained} XP!`
    messageType.value = 'success'
    await loadData()
  } catch (error: any) {
    message.value = error.message || 'Failed to claim daily XP'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

const progressColor = computed(() => {
  if (!xpProgress.value) return 'bg-gray-500'
  const percentage = xpProgress.value.progress_percentage
  if (percentage >= 75) return 'bg-green-500'
  if (percentage >= 50) return 'bg-blue-500'
  if (percentage >= 25) return 'bg-yellow-500'
  return 'bg-gray-500'
})
</script>

<template>
  <div class="xp-page max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">Experience & Leveling</h1>

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

    <!-- XP Progress Card -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">Your Progress</h2>
      <div v-if="xpProgress" class="space-y-4">
        <div class="flex justify-between items-center">
          <span class="text-lg">Level {{ xpProgress.current_level }}</span>
          <span class="text-sm text-gray-600">{{ xpProgress.current_xp }} XP</span>
        </div>

        <!-- Progress Bar -->
        <div class="relative">
          <div class="w-full bg-gray-200 rounded-full h-4">
            <div
              :class="['h-4 rounded-full transition-all duration-500', progressColor]"
              :style="{ width: `${xpProgress.progress_percentage}%` }"
            ></div>
          </div>
          <div class="flex justify-between text-sm text-gray-600 mt-1">
            <span>{{ xpProgress.xp_in_current_level }} XP</span>
            <span>{{ xpProgress.xp_needed_for_next_level }} XP needed for Level {{ xpProgress.next_level }}</span>
          </div>
        </div>

        <div class="text-center">
          <span class="text-3xl font-bold">{{ xpProgress.progress_percentage.toFixed(1) }}%</span>
          <p class="text-sm text-gray-600">to next level</p>
        </div>

        <button
          @click="handleClaimDaily"
          :disabled="isLoading"
          class="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {{ isLoading ? 'Claiming...' : 'Claim Daily Login XP' }}
        </button>
      </div>
    </div>

    <!-- Leaderboard -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">Leaderboard</h2>
      <div v-if="leaderboard.length > 0" class="space-y-3">
        <div
          v-for="(entry, index) in leaderboard"
          :key="entry.username"
          :class="[
            'flex items-center justify-between p-3 rounded',
            index === 0 ? 'bg-yellow-100 dark:bg-yellow-900/20' : '',
            index === 1 ? 'bg-gray-100 dark:bg-gray-700/20' : '',
            index === 2 ? 'bg-orange-100 dark:bg-orange-900/20' : ''
          ]"
        >
          <div class="flex items-center space-x-4">
            <span class="text-lg font-bold w-8">{{ entry.rank }}</span>
            <div v-if="entry.avatar_url" class="w-10 h-10 rounded-full overflow-hidden">
              <img :src="entry.avatar_url" :alt="entry.username" class="w-full h-full object-cover" />
            </div>
            <div>
              <p class="font-semibold">{{ entry.username }}</p>
              <p class="text-sm text-gray-600">Level {{ entry.level }}</p>
            </div>
          </div>
          <div class="text-right">
            <p class="text-lg font-bold">{{ entry.experience_points }}</p>
            <p class="text-sm text-gray-600">XP</p>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-8 text-gray-500">
        <p>No leaderboard data available</p>
      </div>
    </div>
  </div>
</template>