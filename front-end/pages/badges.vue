<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useBadges } from '~/composables/useBadges'
import { useAuth } from '~/composables/useAuth'
import type { Badge, UserBadge } from '~/types/badge'

const { isAuthenticated } = useAuth()
const { getMyBadges, getAvailableBadges, checkEligibility, awardNewBadges, equipBadge } = useBadges()

const myBadges = ref<UserBadge[]>([])
const availableBadges = ref<Badge[]>([])
const eligibleBadges = ref<Badge[]>([])
const isLoading = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

onMounted(async () => {
  if (!isAuthenticated.value) {
    await navigateTo('/users/login')
    return
  }
  await loadBadges()
})

async function loadBadges() {
  try {
    isLoading.value = true
    const [badges, available] = await Promise.all([
      getMyBadges(),
      getAvailableBadges()
    ])
    myBadges.value = badges
    availableBadges.value = available
  } catch (error: any) {
    message.value = 'Failed to load badges'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function checkForNewBadges() {
  try {
    isLoading.value = true
    const eligibility = await checkEligibility()
    eligibleBadges.value = eligibility.eligible_badges || []
  } catch (error: any) {
    message.value = 'Failed to check badge eligibility'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function claimBadges() {
  try {
    isLoading.value = true
    const result = await awardNewBadges()
    if (result.total_awarded > 0) {
      message.value = `Congratulations! You earned ${result.total_awarded} new badge(s)!`
      messageType.value = 'success'
      await loadBadges()
    } else {
      message.value = 'No new badges to claim'
      messageType.value = 'success'
    }
    eligibleBadges.value = []
  } catch (error: any) {
    message.value = error.message || 'Failed to claim badges'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleEquipBadge(badgeId: string) {
  try {
    await equipBadge(badgeId)
    message.value = 'Badge equipped successfully!'
    messageType.value = 'success'
    await loadBadges()
  } catch (error: any) {
    message.value = error.message || 'Failed to equip badge'
    messageType.value = 'error'
  }
}

const tierColors = {
  flat: 'from-gray-400 to-gray-600',
  gradient: 'from-blue-400 to-purple-600',
  holographic: 'from-pink-400 via-purple-400 to-indigo-600'
}

const categoryColors = {
  genre_expert: 'bg-green-100 text-green-800',
  achievement: 'bg-blue-100 text-blue-800',
  social: 'bg-purple-100 text-purple-800',
  rare: 'bg-yellow-100 text-yellow-800'
}
</script>

<template>
  <div class="badges-page max-w-6xl mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Badges</h1>
      <button
        @click="checkForNewBadges"
        :disabled="isLoading"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
      >
        Check for New Badges
      </button>
    </div>

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

    <!-- Eligible Badges -->
    <div v-if="eligibleBadges.length > 0" class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">🎉 New Badges Available!</h2>
      <p class="mb-4">You have {{ eligibleBadges.length }} new badge(s) ready to claim!</p>
      <button
        @click="claimBadges"
        :disabled="isLoading"
        class="bg-yellow-500 text-white px-6 py-2 rounded hover:bg-yellow-600 disabled:opacity-50"
      >
        Claim All Badges
      </button>
    </div>

    <!-- My Badges -->
    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-4">My Badges ({{ myBadges.length }})</h2>
      <div v-if="myBadges.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="userBadge in myBadges"
          :key="userBadge.id"
          :class="[
            'rounded-lg p-6 bg-gradient-to-br shadow-md relative',
            tierColors[userBadge.tier] || tierColors.flat
          ]"
        >
          <div class="text-4xl mb-2">{{ userBadge.icon }}</div>
          <h3 class="text-lg font-semibold">{{ userBadge.name }}</h3>
          <p class="text-sm opacity-80">{{ userBadge.description }}</p>
          <div class="mt-2 flex items-center justify-between">
            <span :class="['px-2 py-1 rounded text-xs', categoryColors[userBadge.category]]">
              {{ userBadge.category }}
            </span>
            <span v-if="userBadge.xp_reward" class="text-xs">+{{ userBadge.xp_reward }} XP</span>
          </div>
          <div v-if="userBadge.is_equipped" class="absolute top-2 right-2">
            <span class="text-xs bg-green-500 text-white px-2 py-1 rounded">Equipped</span>
          </div>
          <button
            v-if="!userBadge.is_equipped"
            @click="handleEquipBadge(userBadge.id)"
            class="mt-3 w-full bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-3 py-1 rounded text-sm"
          >
            Equip
          </button>
        </div>
      </div>
      <div v-else class="text-center py-8 text-gray-500">
        <p>No badges earned yet. Keep using the app to earn badges!</p>
      </div>
    </div>

    <!-- Available Badges -->
    <div>
      <h2 class="text-2xl font-semibold mb-4">All Badges ({{ availableBadges.length }})</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div
          v-for="badge in availableBadges"
          :key="badge.id"
          class="border rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div class="text-3xl mb-2">{{ badge.icon }}</div>
          <h3 class="font-semibold">{{ badge.name }}</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">{{ badge.description }}</p>
          <div class="mt-2 flex items-center justify-between">
            <span :class="['px-2 py-1 rounded text-xs', categoryColors[badge.category]]">
              {{ badge.category }}
            </span>
            <span class="text-xs text-gray-500">+{{ badge.xp_reward }} XP</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>