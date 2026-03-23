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

async function handleSubmit() {
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
    <form @submit.prevent="handleSubmit">
        <div>
            <label>Nom</label>
            <input v-model.trim="form.name" placeholder="Nom" required>
        </div>
        <div>
            <label>Email</label>
            <input v-model.lazy="form.email" type="email" placeholder="Email" required>
        </div>
        <div>
            <label>Âge</label>
            <input v-model.number="form.age" type="number" placeholder="Âge" required>
        </div>
        <div>
            <label>
                <input type="checkbox" v-model="form.isActive">
                Actif
            </label>
        </div>
        <button type="submit">Enregistrer</button>
    </form>
</template>