<template>
  <section aria-labelledby="activity-title" class="sec">
    <div class="sec-head">
      <h2 id="activity-title" class="sec-title">ACTIVITÉ</h2>
      <NuxtLink to="/communaute" class="sec-more">
        Voir tout <i class="ti ti-arrow-right" aria-hidden="true" />
      </NuxtLink>
    </div>

    <ol class="feed" aria-label="Activité récente de la communauté">
      <li v-for="item in items" :key="item.id" class="fi">
        <div
          class="av"
          aria-hidden="true"
        >
          {{ item.user.initials }}
        </div>

        <div class="feed-content">
          <p class="fi-text">
            <span class="fi-name">{{ item.user.initials }}</span>
            {{ item.action }}
            <span class="fi-target">{{ item.target }}</span>
            <template v-if="item.extra">
              <span> - {{ item.extra }}</span>
            </template>
          </p>
          <time class="fi-time" :datetime="item.time">{{ item.time }}</time>
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
