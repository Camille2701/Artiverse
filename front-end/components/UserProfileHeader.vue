<template>
  <div class="relative mb-6">
    <!-- Banner -->
    <div class="h-48 rounded-t-xl bg-gradient-to-r from-accent-movie via-accent-series to-accent-game overflow-hidden relative">
      <div v-if="favoriteMedia.length >= 4" class="absolute inset-0 grid grid-cols-4">
        <img
          v-for="(media, index) in favoriteMedia.slice(0, 4)"
          :key="index"
          :src="media.image"
          :alt="media.title"
          class="w-full h-full object-cover opacity-60 hover:opacity-80 transition-opacity"
        />
      </div>
      <div v-else class="absolute inset-0 flex items-center justify-center">
        <div class="text-center">
          <p class="text-text-primary/80 font-display font-semibold">Personnalisez votre bannière</p>
          <p class="text-text-primary/60 text-sm">Ajoutez des favoris pour créer un collage dynamique</p>
        </div>
      </div>
    </div>

    <!-- Profile info -->
    <div class="bg-bg-secondary rounded-b-xl p-6 relative">
      <!-- Avatar -->
      <div class="absolute -top-12 left-6">
        <div class="relative">
          <div class="w-24 h-24 rounded-full border-4 border-bg-secondary bg-bg-tertiary overflow-hidden">
            <img
              v-if="user.avatar"
              :src="user.avatar"
              :alt="user.username"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-3xl">
              👤
            </div>
          </div>
          <div class="absolute -bottom-1 -right-1 bg-accent text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">
            {{ user.level || '1' }}
          </div>
        </div>
      </div>

      <!-- User info -->
      <div class="ml-32">
        <h1 class="text-2xl font-display font-bold text-text-primary">
          {{ user.username }}
        </h1>
        <p v-if="user.bio" class="text-text-secondary mt-1 font-body">
          {{ user.bio }}
        </p>

        <!-- Gamification stats -->
        <div class="flex items-center gap-6 mt-4">
          <div class="flex items-center gap-2">
            <UIIcon name="star" size="medium" />
            <div>
              <p class="text-text-tertiary text-xs">XP</p>
              <p class="text-text-primary font-semibold">{{ user.experiencePoints || '0' }}</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <UIIcon name="trophy" size="medium" />
            <div>
              <p class="text-text-tertiary text-xs">Niveau</p>
              <p class="text-text-primary font-semibold">{{ user.level || '1' }}</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <UIIcon name="fire" size="medium" />
            <div>
              <p class="text-text-tertiary text-xs">Badges</p>
              <p class="text-text-primary font-semibold">{{ user.badges?.length || '0' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import UIIcon from '~/components/icons/UIIcon.vue';

interface Media {
  id: string
  title: string
  image?: string
  type: string
}

interface User {
  id: string
  username: string
  email: string
  avatar?: string
  bio?: string
  level?: number
  experiencePoints?: number
  badges?: any[]
}

interface Props {
  user: User
  favoriteMedia?: Media[]
}

withDefaults(defineProps<Props>(), {
  favoriteMedia: () => []
})
</script>