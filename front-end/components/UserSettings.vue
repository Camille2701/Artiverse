<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUsers } from '~/composables/useUsers'
import { useAuth } from '~/composables/useAuth'

const { user: currentUser } = useAuth()
const { updateCurrentUser, updatePassword } = useUsers()

const profileForm = ref({
  username: '',
  bio: '',
  avatar_url: ''
})

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const isLoading = ref(false)

onMounted(() => {
  if (currentUser.value) {
    profileForm.value = {
      username: currentUser.value.username,
      bio: currentUser.value.bio || '',
      avatar_url: currentUser.value.avatar_url || ''
    }
  }
})

async function updateProfile() {
  try {
    isLoading.value = true
    await updateCurrentUser(profileForm.value)
    message.value = 'Profile updated successfully!'
    messageType.value = 'success'
  } catch (error: any) {
    message.value = error.message || 'Failed to update profile'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function changePassword() {
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    message.value = 'Passwords do not match'
    messageType.value = 'error'
    return
  }

  try {
    isLoading.value = true
    await updatePassword({
      current_password: passwordForm.value.current_password,
      new_password: passwordForm.value.new_password
    })
    message.value = 'Password updated successfully!'
    messageType.value = 'success'
    passwordForm.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (error: any) {
    message.value = error.message || 'Failed to update password'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="user-settings max-w-2xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-6">Settings</h1>

    <!-- Alert Message -->
    <div
      v-if="message"
      :class="[
        'p-4 rounded mb-6',
        messageType === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
      ]"
    >
      {{ message }}
    </div>

    <!-- Profile Settings -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">Profile Settings</h2>
      <form @submit.prevent="updateProfile" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Username</label>
          <input
            v-model="profileForm.username"
            type="text"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Bio</label>
          <textarea
            v-model="profileForm.bio"
            rows="3"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Avatar URL</label>
          <input
            v-model="profileForm.avatar_url"
            type="url"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          :disabled="isLoading"
          class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {{ isLoading ? 'Saving...' : 'Save Profile' }}
        </button>
      </form>
    </div>

    <!-- Password Settings -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">Change Password</h2>
      <form @submit.prevent="changePassword" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Current Password</label>
          <input
            v-model="passwordForm.current_password"
            type="password"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">New Password</label>
          <input
            v-model="passwordForm.new_password"
            type="password"
            required
            minlength="6"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Confirm New Password</label>
          <input
            v-model="passwordForm.confirm_password"
            type="password"
            required
            minlength="6"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          :disabled="isLoading"
          class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {{ isLoading ? 'Updating...' : 'Update Password' }}
        </button>
      </form>
    </div>
  </div>
</template>