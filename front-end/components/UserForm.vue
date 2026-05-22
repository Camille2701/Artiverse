<script setup lang="ts">
import type { User } from '@/types/user'
import type { Auth } from '@/types/auth'

const props = defineProps<{
  user?: User | null
}>()

const emit = defineEmits<{
  (e: 'submit', data: Partial<User>): void
}>()

const { register, user } = useAuth()
const isLoading = ref(false)
const errorMessage = ref('')

const form = reactive({
    username: '',
    email: '',
    password: '',
    bio: ''
})

const touched = reactive({
  username: false,
  email: false,
  password: false,
  bio: false
})

const errors = reactive({
  username: '',
  email: '',
  password: '',
  bio: ''
})

const baseInputClass =
  'mt-1 block w-full rounded-lg border-2 px-4 py-3 text-sm transition-all duration-200 ease-out focus:outline-none focus:ring-0 focus:shadow-glow'

function validateField(field: 'username' | 'email' | 'password' | 'bio') {
  if (field === 'username') {
    errors.username = form.username.trim().length >= 3 ? '' : 'Le nom d\'utilisateur doit contenir au moins 3 caractères.'
  }

  if (field === 'email') {
    if (!form.email.trim()) {
      errors.email = 'L\'email est requis.'
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      errors.email = emailRegex.test(form.email) ? '' : 'L\'email est invalide.'
    }
  }

  if (field === 'password') {
    errors.password = form.password.length >= 8 ? '' : 'Le mot de passe doit contenir au moins 8 caractères.'
  }

  if (field === 'bio') {
    errors.bio = form.bio.length <= 500 ? '' : 'La biographie ne peut pas dépasser 500 caractères.'
  }
}

function inputClass(field: 'username' | 'email' | 'password' | 'bio') {
  const hasError = touched[field] && !!errors[field]
  return [
    baseInputClass,
    hasError
      ? 'bg-red-950/30 border-red-500 text-red-100 placeholder-red-300/50 focus:border-red-400'
      : 'bg-bg-tertiary/50 border-border-color text-text-primary placeholder-text-tertiary hover:border-border-color-light focus:border-accent',
    hasError ? 'shadow-[0_0_15px_rgba(239,68,68,0.3)]' : ''
  ]
}

function markTouchedAndValidate(field: 'username' | 'email' | 'password' | 'bio') {
  touched[field] = true
  validateField(field)
}

function validateForm() {
  markTouchedAndValidate('username')
  markTouchedAndValidate('email')
  markTouchedAndValidate('password')
  markTouchedAndValidate('bio')
  return !errors.username && !errors.email && !errors.password && !errors.bio
}

async function handleSubmit() {
  if (!validateForm()) {
    return
  }

  errorMessage.value = ''
  isLoading.value = true

  try {
    await register({
      username: form.username,
      email: form.email,
      password: form.password,
      bio: form.bio
    })

    if (user.value) {
      await navigateTo(`/users/${user.value.id}`)
    }
  } catch (error: unknown) {
    console.error('Registration error:', error)
    if (error && typeof error === 'object' && 'statusMessage' in error) {
      errorMessage.value = String((error as { statusMessage?: string }).statusMessage || 'Erreur lors de l\'inscription')
    } else {
      errorMessage.value = 'Erreur lors de l\'inscription'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <form class="space-y-5" novalidate @submit.prevent="handleSubmit">
    <p class="text-sm text-text-secondary font-body">Crée ton compte en complétant les informations ci-dessous.</p>
    <div>
      <label class="block text-sm font-medium text-text-primary mb-2 font-display">Nom d'utilisateur</label>
      <input
        v-model.trim="form.username"
        :class="inputClass('username')"
        placeholder="tonpseudo"
        required
        @blur="markTouchedAndValidate('username')"
      >
      <p v-if="touched.username && errors.username" class="mt-2 text-xs text-red-400 font-medium">{{ errors.username }}</p>
    </div>
    <div>
      <label class="block text-sm font-medium text-text-primary mb-2 font-display">Email</label>
      <input
        v-model.lazy="form.email"
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
        v-model="form.password"
        :class="inputClass('password')"
        type="password"
        placeholder="•••••••• (8 caractères minimum)"
        required
        @blur="markTouchedAndValidate('password')"
      >
      <p v-if="touched.password && errors.password" class="mt-2 text-xs text-red-400 font-medium">{{ errors.password }}</p>
    </div>
    <div>
      <label class="block text-sm font-medium text-text-primary mb-2 font-display">Biographie (optionnel)</label>
      <textarea
        v-model="form.bio"
        :class="inputClass('bio')"
        rows="3"
        placeholder="Parle-nous un peu de toi..."
        @blur="markTouchedAndValidate('bio')"
      ></textarea>
      <p v-if="touched.bio && errors.bio" class="mt-2 text-xs text-red-400 font-medium">{{ errors.bio }}</p>
    </div>
    <button
      class="btn-primary w-full py-3 text-base font-display font-semibold"
      type="submit"
      :disabled="isLoading"
    >
      {{ isLoading ? 'Inscription...' : 'S\'inscrire' }}
    </button>
    <p v-if="errorMessage" class="text-sm text-red-400 font-medium bg-red-950/50 border border-red-500/30 rounded-lg p-4">{{ errorMessage }}</p>
  </form>
</template>