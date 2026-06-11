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
  <form class="auth-form" novalidate @submit.prevent="handleLogin">
    <div>
      <label class="auth-label">Email</label>
      <input
        v-model.trim="email"
        :class="inputClass('email')"
        type="email"
        placeholder="nom@exemple.com"
        required
        @blur="markTouchedAndValidate('email')"
      >
      <p v-if="touched.email && errors.email" class="auth-error">{{ errors.email }}</p>
    </div>
    <div>
      <label class="auth-label">Mot de passe</label>
      <input
        v-model="password"
        :class="inputClass('password')"
        type="password"
        placeholder="Mot de passe"
        required
        @blur="markTouchedAndValidate('password')"
      >
      <p v-if="touched.password && errors.password" class="auth-error">{{ errors.password }}</p>
    </div>
    <button
      class="auth-submit btn-cta"
      type="submit"
      :disabled="isLoading"
    >
      {{ isLoading ? 'Connexion...' : 'Se connecter' }}
    </button>
    <p v-if="errorMessage" class="auth-error auth-error--banner">{{ errorMessage }}</p>
  </form>
</template>

<style scoped>
.auth-form {
  display: grid;
  gap: 18px;
}

.auth-label {
  display: inline-block;
  margin-bottom: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--c-purple-pale);
}

.auth-error {
  margin-top: 8px;
  font-size: 0.88rem;
  color: var(--c-pink);
}

.auth-error--banner {
  padding: 12px 14px;
  border: 0.5px solid rgba(237, 147, 177, 0.28);
  border-radius: var(--radius-md);
  background: rgba(75, 21, 40, 0.35);
}

.auth-submit {
  width: 100%;
  justify-content: center;
}
</style>