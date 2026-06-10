<template>
  <section aria-labelledby="activity-title">
    <div class="sec-header">
      <h2 id="activity-title" class="sec-title">ACTIVITÉ</h2>
      <NuxtLink to="/communaute" class="sec-more">
        Voir tout <i class="ti ti-arrow-right" aria-hidden="true" />
      </NuxtLink>
    </div>

    <ol class="feed" aria-label="Activité récente de la communauté">
      <li v-for="item in items" :key="item.id" class="feed-item">
        <div
          class="avatar"
          :style="{ background: item.user.color, color: item.user.textColor }"
          aria-hidden="true"
        >
          {{ item.user.initials }}
        </div>

        <div class="feed-content">
          <p class="feed-text">
            <span class="feed-name">{{ item.user.initials }}</span>
            {{ item.action }}
            <span class="feed-target">{{ item.target }}</span>
            <template v-if="item.extra">
              <span v-if="item.extraType === 'badge'" class="feed-badge">{{ item.extra }}</span>
              <span v-else-if="item.extraType === 'quote'" class="feed-quote">{{ item.extra }}</span>
              <span v-else class="feed-note">— {{ item.extra }}</span>
            </template>
          </p>
          <time class="feed-time" :datetime="item.time">{{ item.time }}</time>
        </div>
      </li>
    </ol>
  </section>
</template>

<script setup lang="ts">
import type { ActivityItem } from '~/types'
defineProps<{ items: ActivityItem[] }>()
</script>

<style scoped>
/* visual rules provided by global CSS */
</style>
