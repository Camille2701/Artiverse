<template>
  <div class="max-w-6xl mx-auto">
    <div class="mb-6">
      <h1 class="text-3xl font-display font-bold text-text-primary">Mon Profil</h1>
      <p class="text-text-secondary mt-2 font-body">Gérez votre identité culturelle et découvrez vos statistiques</p>
    </div>

    <UserProfile
      :user="mockUser"
      :stats="mockStats"
      :badges="mockBadges"
      :favorite-media="mockFavoriteMedia"
      :recent-activity="mockRecentActivity"
    />
  </div>
</template>

<script setup lang="ts">
import UserProfile from '~/components/UserProfile.vue'

// Mock data - replace with real API calls
const mockUser = {
  id: '1',
  username: 'Cinéphile Passionné',
  email: 'user@example.com',
  avatar: undefined,
  bio: 'Amateur de cinéma indépendant et de jeux vidéo rétro',
  level: 12,
  experiencePoints: 3450
}

const mockStats = {
  movies: 45,
  series: 23,
  games: 31,
  books: 18
}

const mockBadges = [
  {
    id: '1',
    name: 'Cinéphile Débutant',
    description: 'A regardé 10 films',
    icon: '🎬',
    level: 'Débutant',
    style: 'flat',
    mediaType: 'movie'
  },
  {
    id: '2',
    name: 'Séries Binge-Watcher',
    description: 'A terminé 5 séries',
    icon: '📺',
    level: 'Intermédiaire',
    style: 'gradient',
    mediaType: 'series'
  },
  {
    id: '3',
    name: 'Gamer Hardcore',
    description: 'A joué à 20 jeux différents',
    icon: '🎮',
    level: 'Expert',
    style: 'holographic',
    mediaType: 'game'
  },
  {
    id: '4',
    name: 'Lecteur Passionné',
    description: 'A lu 15 livres',
    icon: '📚',
    level: 'Intermédiaire',
    style: 'gradient',
    mediaType: 'book'
  }
]

const mockFavoriteMedia = [
  {
    id: '1',
    title: 'Inception',
    image: 'https://via.placeholder.com/400x600',
    type: 'movie'
  },
  {
    id: '2',
    title: 'Breaking Bad',
    image: 'https://via.placeholder.com/400x600',
    type: 'series'
  },
  {
    id: '3',
    title: 'The Legend of Zelda',
    image: 'https://via.placeholder.com/400x600',
    type: 'game'
  },
  {
    id: '4',
    title: 'Dune',
    image: 'https://via.placeholder.com/400x600',
    type: 'book'
  }
]

const mockRecentActivity = [
  {
    id: '1',
    icon: '⭐',
    title: 'Nouveau badge débloqué',
    description: 'Vous avez obtenu le badge "Cinéphile Débutant"',
    date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
  },
  {
    id: '2',
    icon: '🎬',
    title: 'Film regardé',
    description: 'Vous avez regardé "Inception"',
    date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString()
  },
  {
    id: '3',
    icon: '📝',
    title: 'Critique publiée',
    description: 'Vous avez publié une critique pour "Breaking Bad"',
    date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()
  }
]
</script>