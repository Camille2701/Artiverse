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
  'mt-1 block w-full rounded-md border px-3 py-2 text-sm transition-all duration-200 ease-out focus:outline-none focus:ring-2'

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
      ? 'border-red-500 hover:border-red-600 focus:border-red-500 focus:ring-red-500 active:border-red-600 active:ring-red-500/70'
      : 'border-slate-300 hover:border-slate-400 focus:border-blue-500 focus:ring-blue-500 active:border-blue-600 active:ring-blue-500/70'
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
  <form class="space-y-4" novalidate @submit.prevent="handleSubmit">
    <p class="text-sm text-slate-600">Crée ton compte en complétant les informations ci-dessous.</p>
    <div>
      <label class="text-sm font-medium text-slate-700">Nom d'utilisateur</label>
      <input
        v-model.trim="form.username"
        :class="inputClass('username')"
        placeholder="Nom d'utilisateur"
        required
        @blur="markTouchedAndValidate('username')"
      >
      <p v-if="touched.username && errors.username" class="mt-1 text-xs text-red-600">{{ errors.username }}</p>
    </div>
    <div>
      <label class="text-sm font-medium text-slate-700">Email</label>
      <input
        v-model.lazy="form.email"
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
        v-model="form.password"
        :class="inputClass('password')"
        type="password"
        placeholder="Mot de passe (8 caractères minimum)"
        required
        @blur="markTouchedAndValidate('password')"
      >
      <p v-if="touched.password && errors.password" class="mt-1 text-xs text-red-600">{{ errors.password }}</p>
    </div>
    <div>
      <label class="text-sm font-medium text-slate-700">Biographie (optionnel)</label>
      <textarea
        v-model="form.bio"
        :class="inputClass('bio')"
        rows="3"
        placeholder="Parle-nous un peu de toi..."
        @blur="markTouchedAndValidate('bio')"
      ></textarea>
      <p v-if="touched.bio && errors.bio" class="mt-1 text-xs text-red-600">{{ errors.bio }}</p>
    </div>
    <button
      class="btn-accent"
      type="submit"
      :disabled="isLoading"
    >
      {{ isLoading ? 'Inscription...' : 'S\'inscrire' }}
    </button>
    <p v-if="errorMessage" class="text-sm text-red-600">{{ errorMessage }}</p>
  </form>
</template>