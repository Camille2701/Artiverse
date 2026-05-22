<template>
  <div
    class="badge inline-flex items-center gap-2"
    :class="badgeClasses"
  >
    <span v-if="badge.icon" class="text-lg">{{ badge.icon }}</span>
    <div class="flex flex-col">
      <span class="font-semibold">{{ badge.name }}</span>
      <span v-if="badge.description" class="text-xs opacity-75">{{ badge.description }}</span>
    </div>
    <span v-if="badge.level" class="ml-auto text-xs opacity-75">{{ badge.level }}</span>
  </div>
</template>

<script setup lang="ts">
interface Badge {
  id: string
  name: string
  description?: string
  icon?: string
  level?: string
  style: 'flat' | 'gradient' | 'glass' | 'holographic'
  mediaType?: 'movie' | 'series' | 'game' | 'book'
}

interface Props {
  badge: Badge
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md'
})

const badgeClasses = computed(() => {
  const classes = []

  // Size classes
  switch (props.size) {
    case 'sm':
      classes.push('px-2 py-1 text-xs')
      break
    case 'md':
      classes.push('px-3 py-1.5 text-sm')
      break
    case 'lg':
      classes.push('px-4 py-2 text-base')
      break
  }

  // Style classes
  switch (props.badge.style) {
    case 'flat':
      classes.push('badge-flat')
      break
    case 'gradient':
      classes.push('badge-gradient')
      if (props.badge.mediaType) {
        classes.push(getMediaGradientClass(props.badge.mediaType))
      }
      break
    case 'glass':
      classes.push('badge-glass')
      break
    case 'holographic':
      classes.push('badge-holographic')
      break
  }

  return classes.join(' ')
})

const getMediaGradientClass = (mediaType: string) => {
  switch (mediaType) {
    case 'movie':
      return 'from-accent-movie to-accent-movie-hover'
    case 'series':
      return 'from-accent-series to-accent-series-hover'
    case 'game':
      return 'from-accent-game to-accent-game-hover'
    case 'book':
      return 'from-accent-book to-accent-book-hover'
    default:
      return 'from-accent to-accent-hover'
  }
}
</script>