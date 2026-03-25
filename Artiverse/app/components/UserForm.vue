<script setup lang="ts">
import type { User } from '@/types/user'

const props = defineProps<{
  user?: User | null
}>()

const emit = defineEmits<{
  (e: 'submit', data: Partial<User>): void
}>()

const form = reactive({
    name: '',
    email: '',
    isActive: false,
    isComplete: false,
    age: 0
})

const touched = reactive({
  name: false,
  email: false,
  age: false
})

const errors = reactive({
  name: '',
  email: '',
  age: ''
})

const baseInputClass =
  'mt-1 block w-full rounded-md border px-3 py-2 text-sm transition-all duration-200 ease-out focus:outline-none focus:ring-2'

function validateField(field: 'name' | 'email' | 'age') {
  if (field === 'name') {
    errors.name = form.name.trim() ? '' : 'Le nom est requis.'
  }

  if (field === 'email') {
    if (!form.email.trim()) {
      errors.email = 'L\'email est requis.'
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      errors.email = emailRegex.test(form.email) ? '' : 'L\'email est invalide.'
    }
  }

  if (field === 'age') {
    errors.age = Number(form.age) > 0 ? '' : 'L\'âge doit être supérieur à 0.'
  }
}

function inputClass(field: 'name' | 'email' | 'age') {
  const hasError = touched[field] && !!errors[field]
  return [
    baseInputClass,
    hasError
      ? 'border-red-500 hover:border-red-600 focus:border-red-500 focus:ring-red-500 active:border-red-600 active:ring-red-500/70'
      : 'border-slate-300 hover:border-slate-400 focus:border-blue-500 focus:ring-blue-500 active:border-blue-600 active:ring-blue-500/70'
  ]
}

function markTouchedAndValidate(field: 'name' | 'email' | 'age') {
  touched[field] = true
  validateField(field)
}

function validateForm() {
  markTouchedAndValidate('name')
  markTouchedAndValidate('email')
  markTouchedAndValidate('age')
  return !errors.name && !errors.email && !errors.age
}

async function handleSubmit() {
  if (!validateForm()) {
    return
  }

  const newId = Date.now()
  
  const userData = {
    id: newId,
    name: form.name,
    email: form.email,
    isActive: form.isActive,
    age: form.age,
    avatar: `https://i.pravatar.cc/150?img=${Math.floor(Math.random() * 70)}`
  }
  
  emit('submit', userData)
  
  sessionStorage.setItem(`user_${newId}`, JSON.stringify(userData))
  
  await navigateTo(`/users/${newId}`)
}
</script>

<template>
  <form class="space-y-4" novalidate @submit.prevent="handleSubmit">
    <p class="text-sm text-slate-600">Crée ton compte en complétant les informations ci-dessous.</p>
    <div>
      <label class="text-sm font-medium text-slate-700">Nom</label>
      <input
        v-model.trim="form.name"
        :class="inputClass('name')"
        placeholder="Nom"
        required
        @blur="markTouchedAndValidate('name')"
      >
      <p v-if="touched.name && errors.name" class="mt-1 text-xs text-red-600">{{ errors.name }}</p>
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
      <label class="text-sm font-medium text-slate-700">Âge</label>
      <input
        v-model.number="form.age"
        :class="inputClass('age')"
        type="number"
        placeholder="Âge"
        required
        @blur="markTouchedAndValidate('age')"
      >
      <p v-if="touched.age && errors.age" class="mt-1 text-xs text-red-600">{{ errors.age }}</p>
    </div>
    <div>
      <label class="inline-flex items-center gap-2 text-sm text-slate-700">
        <input class="h-4 w-4 rounded border-slate-300 text-blue-600 transition-all duration-200 ease-out hover:border-slate-400 focus:ring-2 focus:ring-blue-500 active:border-blue-600 active:ring-blue-500/70" type="checkbox" v-model="form.isActive">
        Actif
      </label>
    </div>
    <button
      class="w-full rounded-md bg-accent px-4 py-2 text-white transition-all duration-200 ease-out hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 active:bg-accent-hover"
      type="submit"
    >
      Enregistrer
    </button>
  </form>
</template>