<script setup lang="ts">
const { login, user } = useAuth()
const { getErrorMessage } = useApi()
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
  'mt-1 block w-full rounded-lg border-2 px-4 py-3 text-sm transition-all duration-200 ease-out focus:outline-none focus:ring-0 focus:shadow-glow'

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
      ? 'bg-red-950/30 border-red-500 text-red-100 placeholder-red-300/50 focus:border-red-400'
      : 'bg-bg-tertiary/50 border-border-color text-text-primary placeholder-text-tertiary hover:border-border-color-light focus:border-accent',
    hasError ? 'shadow-[0_0_15px_rgba(239,68,68,0.3)]' : ''
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
    errorMessage.value = getErrorMessage(error as any || { statusCode: 400, statusMessage: 'Erreur de connexion' })
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <form class="space-y-5" novalidate @submit.prevent="handleLogin">
    <p class="text-sm text-text-secondary font-body">Renseigne tes identifiants pour accéder à ton espace.</p>
    <div>
      <label class="block text-sm font-medium text-text-primary mb-2 font-display">Email</label>
      <input
        v-model.trim="email"
        :class="inputClass('email')"
        type="email"
        placeholder="ton@email.com"
        required
        @blur="markTouchedAndValidate('email')"
      >
      <p v-if="touched.email && errors.email" class="mt-2 text-xs text-red-400 font-medium">{{ errors.email }}</p>
    </div>
    <div>
      <label class="block text-sm font-medium text-text-primary mb-2 font-display">Mot de passe</label>
      <input
        v-model="password"
        :class="inputClass('password')"
        type="password"
        placeholder="••••••••"
        required
        @blur="markTouchedAndValidate('password')"
      >
      <p v-if="touched.password && errors.password" class="mt-2 text-xs text-red-400 font-medium">{{ errors.password }}</p>
    </div>
    <button
      class="btn-primary w-full py-3 text-base font-display font-semibold"
      type="submit"
      :disabled="isLoading"
    >
      <span v-if="isLoading" class="flex items-center justify-center gap-2">
        <span class="spinner !w-5 !h-5 !border-2"></span>
        Connexion...
      </span>
      <span v-else>Se connecter</span>
    </button>
    <div v-if="errorMessage" class="rounded-lg bg-red-950/50 border border-red-500/30 p-4">
      <p class="text-sm font-medium text-red-200">{{ errorMessage }}</p>
    </div>
  </form>
</template>