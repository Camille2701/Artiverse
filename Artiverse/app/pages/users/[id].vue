<script setup lang="ts">
import type { User } from '@/types/user'



useHead({
  title: "Artisverse",
  meta: [
    { name: "Page de consultation d'un utilisateur", content: "Consultation d'un utilisateur"}
  ]
})

const route = useRoute()
const userId = route.params.id as string

const user = ref<User | null>(null)
const error = ref(false)

onMounted(() => {
  const stored = sessionStorage.getItem(`user_${userId}`)
  if (stored) {
    user.value = JSON.parse(stored)
    return
  }

  $fetch<User[]>('/api/users')
    .then(users => {
      user.value = users.find(u => u.id === Number(userId)) || null
      if (!user.value) {
        error.value = true
      }
    })
    .catch(() => {
      error.value = true
    })
})
</script>

<template>
  <div class="user-detail-page">
    <div v-if="error" class="error">
      <h1>Utilisateur introuvable</h1>
      <NuxtLink to="/" class="btn">Retour à l'accueil</NuxtLink>
    </div>

    <div v-else-if="user" class="user-detail">
      <div class="header">
        <img :src="user.avatar" :alt="user.name" class="avatar" />
        <div>
          <h1>{{ user.name }}</h1>
          <span class="status" :class="{ active: user.isActive }">
            {{ user.isActive ? '✓ Actif' : '○ Inactif' }}
          </span>
        </div>
      </div>

      <div class="info-grid">
        <div class="info-item">
          <strong>Email</strong>
          <span>{{ user.email }}</span>
        </div>
        <div class="info-item">
          <strong>Âge</strong>
          <span>{{ user.age }} ans</span>
        </div>
        <div class="info-item">
          <strong>ID</strong>
          <span>#{{ user.id }}</span>
        </div>
        <div class="info-item">
          <strong>Rôle</strong>
          <span>{{ user.role }}</span>
        </div>
      </div>

      <div class="actions">
        <NuxtLink to="/users/new" class="btn btn-secondary">
          Créer un utilisateur
        </NuxtLink>
        <NuxtLink to="/" class="btn btn-primary">
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>

    <div v-else class="loading">
      Chargement...
    </div>
  </div>
</template>

<style scoped>
.user-detail-page {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
}

.user-detail {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid #e5e7eb;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
}

.header h1 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
}

.status {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.875rem;
}

.status.active {
  background: #d1fae5;
  color: #065f46;
}

.status:not(.active) {
  background: #fee2e2;
  color: #991b1b;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.info-item {
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.info-item strong {
  display: block;
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.info-item span {
  color: #1f2937;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
}

.error, .loading {
  text-align: center;
  padding: 2rem;
}

.error h1 {
  color: #ef4444;
  margin-bottom: 1rem;
}
</style>
