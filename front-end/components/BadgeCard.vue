<script setup lang="ts">
// @ts-ignore
import type { UserBadge, BadgeProgress } from '~/types/badge'
// @ts-ignore
import { BadgeTier, BadgeCategory } from '~/types/badge'
import UIIcon from '~/components/icons/UIIcon.vue';

interface Props {
  badge: UserBadge | BadgeProgress
  showProgress?: boolean
  size?: 'small' | 'medium' | 'large'
  clickable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showProgress: false,
  size: 'medium',
  clickable: true
})

const emit = defineEmits<{
  click: [badge: UserBadge | BadgeProgress]
}>()

function getTierStyle(tier: string) {
  switch (tier) {
    case BadgeTier.Flat:
      return 'bg-gradient-to-br from-slate-100 to-slate-200 border-slate-300'
    case BadgeTier.Gradient:
      return 'bg-gradient-to-br from-purple-100 to-blue-100 border-purple-300'
    case BadgeTier.Holographic:
      return 'bg-gradient-to-br from-yellow-100 via-pink-100 to-blue-100 border-yellow-300 shadow-lg'
    default:
      return 'bg-slate-100 border-slate-300'
  }
}

function getCategoryColor(category: string) {
  switch (category) {
    case BadgeCategory.GenreExpert:
      return 'text-purple-600'
    case BadgeCategory.Achievement:
      return 'text-blue-600'
    case BadgeCategory.Social:
      return 'text-green-600'
    case BadgeCategory.Rare:
      return 'text-yellow-600'
    default:
      return 'text-slate-600'
  }
}

function getCategoryLabel(category: string) {
  switch (category) {
    case BadgeCategory.GenreExpert:
      return 'Expert de genre'
    case BadgeCategory.Achievement:
      return 'Succès'
    case BadgeCategory.Social:
      return 'Social'
    case BadgeCategory.Rare:
      return 'Rare'
    default:
      return category
  }
}

function getSizeClasses() {
  switch (props.size) {
    case 'small':
      return 'w-16 h-16 text-2xl'
    case 'medium':
      return 'w-24 h-24 text-4xl'
    case 'large':
      return 'w-32 h-32 text-5xl'
    default:
      return 'w-24 h-24 text-4xl'
  }
}

function isUserBadge(badge: UserBadge | BadgeProgress): badge is UserBadge {
  return 'is_equipped' in badge
}

function getDisplayName(badge: UserBadge | BadgeProgress) {
  return isUserBadge(badge) ? badge.name : badge.badge_name
}

function getProgress(badge: UserBadge | BadgeProgress) {
  if (!isUserBadge(badge)) {
    return {
      current: badge.current,
      target: badge.target,
      percentage: badge.percentage,
      is_complete: badge.is_complete
    }
  }
  return badge.progress || { current: 0, target: 0, percentage: 0, is_complete: true }
}

const isComplete = computed(() => {
  if (!isUserBadge(props.badge)) {
    return props.badge.is_complete
  }
  return true // User badges are always earned
})
</script>

<template>
  <div
    class="relative group cursor-pointer"
    :class="{ 'cursor-default': !clickable }"
    @click="clickable ? emit('click', badge) : null"
  >
    <!-- Badge card -->
    <div
      class="rounded-full flex items-center justify-center border-2 transition-all duration-300"
      :class="[
        getTierStyle(isUserBadge(badge) ? badge.tier : 'flat'),
        getSizeClasses(),
        {
          'hover:scale-110 hover:shadow-xl': clickable,
          'opacity-60 grayscale': !isComplete,
          'ring-2 ring-accent ring-offset-2 ring-offset-white dark:ring-offset-bg-primary': isUserBadge(badge) && badge.is_equipped
        }
      ]"
      :title="getDisplayName(badge)"
    >
      <UIIcon :name="badge.icon as any || 'trophy'" size="large" />
    </div>

    <!-- Holographic effect for rare badges -->
    <div
      v-if="isUserBadge(badge) && badge.tier === BadgeTier.Holographic"
      class="absolute inset-0 rounded-full bg-gradient-to-br from-yellow-200 via-pink-200 to-blue-200 opacity-0 group-hover:opacity-30 transition-opacity duration-500 animate-pulse"
    ></div>

    <!-- Tooltip -->
    <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none z-10">
      <div class="bg-white dark:bg-bg-secondary border border-gray-200 dark:border-border-color rounded-lg shadow-lg p-3">
        <h4 class="font-bold text-gray-900 dark:text-text-primary text-sm mb-1">
          {{ getDisplayName(badge) }}
        </h4>
        <p class="text-xs text-gray-600 dark:text-text-secondary mb-2">
          {{ isUserBadge(badge) ? badge.description : '' }}
        </p>
        <div class="flex items-center justify-between text-xs">
          <span :class="getCategoryColor(isUserBadge(badge) ? badge.category : 'achievement')">
            {{ isUserBadge(badge) ? getCategoryLabel(badge.category) : getCategoryLabel('achievement') }}
          </span>
          <span v-if="isUserBadge(badge) && badge.xp_reward" class="text-yellow-600 dark:text-yellow-400">
            +{{ badge.xp_reward }} XP
          </span>
        </div>

        <!-- Progress bar -->
        <div v-if="showProgress && !isComplete" class="mt-2">
          <div class="flex justify-between text-xs text-gray-600 dark:text-text-secondary mb-1">
            <span>Progression</span>
            <span>{{ getProgress(badge).current }}/{{ getProgress(badge).target }}</span>
          </div>
          <div class="h-1.5 bg-gray-200 dark:bg-bg-tertiary rounded-full overflow-hidden">
            <div
              class="h-full bg-accent transition-all duration-500"
              :style="{ width: `${getProgress(badge).percentage}%` }"
            ></div>
          </div>
        </div>

        <!-- Earned date -->
        <div v-if="isUserBadge(badge) && badge.earned_at" class="mt-2 text-xs text-gray-500 dark:text-text-secondary">
          Gagné le {{ new Date(badge.earned_at).toLocaleDateString('fr-FR') }}
        </div>
      </div>

      <!-- Arrow -->
      <div class="absolute top-full left-1/2 -translate-x-1/2 -mt-1">
        <div class="border-8 border-transparent border-t-white dark:border-t-bg-secondary"></div>
      </div>
    </div>

    <!-- Equipped indicator -->
    <div
      v-if="isUserBadge(badge) && badge.is_equipped"
      class="absolute -top-1 -right-1 bg-accent text-white rounded-full w-5 h-5 flex items-center justify-center text-xs"
      title="Badge équipé"
    >
      <UIIcon name="check" size="small" />
    </div>

    <!-- Incomplete indicator -->
    <div
      v-if="!isComplete"
      class="absolute -bottom-1 -right-1 bg-gray-400 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs"
      title="Non complété"
    >
      <UIIcon name="lock" size="small" />
    </div>
  </div>
</template>