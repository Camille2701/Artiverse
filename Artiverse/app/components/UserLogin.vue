<script setup lang="ts">
const { login, user } = useAuth()
const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  errorMessage.value = ''
  isLoading.value = true

  try {
    await login({ email: email.value, password: password.value })
    if (user.value) {
      await navigateTo(`/users/${user.value.id}`)
    }
  } catch (error: unknown) {
    if (error && typeof error === 'object' && 'statusMessage' in error) {
      errorMessage.value = String((error as { statusMessage?: string }).statusMessage || 'Erreur de connexion')
    } else {
      errorMessage.value = 'Erreur de connexion'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <form @submit.prevent="handleLogin">
    <input v-model.trim="email" type="email" placeholder="Email" required />
    <input v-model="password" type="password" placeholder="Mot de passe" required />
    <button type="submit" :disabled="isLoading">
      {{ isLoading ? 'Connexion...' : 'Se connecter' }}
    </button>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </form>
</template>