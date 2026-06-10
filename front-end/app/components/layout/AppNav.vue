<template>
  <nav class="nav" role="navigation" aria-label="Navigation principale">
    <NuxtLink to="/" class="nav-logo" aria-label="Artiverse — Accueil">
        <img src="/logo.png" alt="Logo Artiverse">
    </NuxtLink>

    <ul class="nav-links" role="list">
      <li v-for="link in links" :key="link.to">
        <NuxtLink :to="link.to" class="nav-link" :aria-current="isActive(link.to) ? 'page' : undefined">
          {{ link.label }}
        </NuxtLink>
      </li>
    </ul>

    <div class="nav-right">
      <template v-if="isAuthenticated">
        <button class="nav-avatar" aria-label="Menu du compte">
          <img v-if="user?.avatar" :src="user.avatar" :alt="user.name" class="nav-avatar-img" />
          <span v-else>{{ userInitials }}</span>
        </button>
      </template>

      <template v-else>
          <NuxtLink to="/users/new" class="btn-join gold">Inscription</NuxtLink>
        <NuxtLink to="/users/login" class="btn-join btn-join--outline">Connexion</NuxtLink>
      </template>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const { user, isAuthenticated } = useAuth()

const links = [
  { label: 'Découvrir',    to: '/'           },
  { label: 'Films',        to: '/films'       },
  { label: 'Séries',       to: '/series'      },
  { label: 'Jeux',         to: '/jeux'        },
  { label: 'Livres',       to: '/livres'      },
  { label: 'Communauté',   to: '/communaute'  },
]

const isActive = (to: string) => route.path === to

const userInitials = computed(() => {
  const name = user.value?.name?.trim() ?? ''
  if (!name) return 'AC'

  return name
    .split(/\s+/)
    .slice(0, 2)
    .map((part: string) => part[0]?.toUpperCase() ?? '')
    .join('')
})
</script>

<style scoped>
.nav-avatar-img{width:100%;height:100%;object-fit:cover;border-radius:50%}
</style>
