<script setup lang="ts">
const { login, user } = useAuth()
const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const touched = reactive({
  email: false,
  password: false
})

const errors = reactive({
  email: '',
  password: ''
})

const baseInputClass =
  'mt-1 block w-full rounded-md border px-3 py-2 text-sm transition-all duration-200 ease-out focus:outline-none focus:ring-2'

function validateField(field: 'email' | 'password') {
  if (field === 'email') {
    if (!email.value.trim()) {
      errors.email = 'L\'email est requis.'
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      errors.email = emailRegex.test(email.value) ? '' : 'L\'email est invalide.'
    }
  }

  if (field === 'password') {
    errors.password = password.value ? '' : 'Le mot de passe est requis.'
  }
}

function inputClass(field: 'email' | 'password') {
  const hasError = touched[field] && !!errors[field]
  return [
    baseInputClass,
    hasError
      ? 'border-red-500 hover:border-red-600 focus:border-red-500 focus:ring-red-500 active:border-red-600 active:ring-red-500/70'
      : 'border-slate-300 hover:border-slate-400 focus:border-blue-500 focus:ring-blue-500 active:border-blue-600 active:ring-blue-500/70'
  ]
}

function markTouchedAndValidate(field: 'email' | 'password') {
  touched[field] = true
  validateField(field)
}

function validateForm() {
  markTouchedAndValidate('email')
  markTouchedAndValidate('password')
  return !errors.email && !errors.password
}

async function handleLogin() {
  if (!validateForm()) {
    return
  }

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
  <form class="space-y-4" novalidate @submit.prevent="handleLogin">
    <p class="text-sm text-slate-600">Renseigne tes identifiants pour accéder à ton espace.</p>
    <div>
      <label class="text-sm font-medium text-slate-700">Email</label>
      <input
        v-model.trim="email"
        :class="inputClass('email')"
        type="email"
        placeholder="Email"
        required
        @blur="markTouchedAndValidate('email')"
      >
      <p v-if="touched.email && errors.email" class="mt-1 text-xs text-red-600">{{ errors.email }}</p>
    </div>
    <div>
      <label class="text-sm font-medium text-slate-700">Mot de passe</label>
      <input
        v-model="password"
        :class="inputClass('password')"
        type="password"
        placeholder="Mot de passe"
        required
        @blur="markTouchedAndValidate('password')"
      >
      <p v-if="touched.password && errors.password" class="mt-1 text-xs text-red-600">{{ errors.password }}</p>
    </div>
    <button
      class="btn-accent"
      type="submit"
      :disabled="isLoading"
    >
      {{ isLoading ? 'Connexion...' : 'Se connecter' }}
    </button>
    <p v-if="errorMessage" class="text-sm text-red-600">{{ errorMessage }}</p>
  </form>
</template>