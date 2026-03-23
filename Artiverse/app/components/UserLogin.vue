<script setup lang="ts">
const { login } = useAuth()
const email = ref('')
const password = ref('')

async function handleLogin() {
  await login({ email: email.value, password: password.value })
  navigateTo('/dashboard')
}
</script>

<template>
  <input v-model="email" placeholder="Email" />
  <input v-model="password" type="password" placeholder="Mot de passe" />
  <button @click="handleLogin">Se connecter</button>
</template>