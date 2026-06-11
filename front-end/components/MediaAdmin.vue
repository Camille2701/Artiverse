<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMedia } from '~/composables/useMedia'
import type { Media, MediaCreate } from '~/types/media'

const { getAllMedia, createMedia, updateMedia, deleteMedia } = useMedia()

const mediaList = ref<Media[]>([])
const isLoading = ref(false)
const showCreateForm = ref(false)
const editingMedia = ref<Media | null>(null)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

const createForm = ref<MediaCreate>({
  media_type: 'movie' as any,
  title: '',
  synopsis: '',
  release_date: ''
})

const searchQuery = ref('')

onMounted(async () => {
  await loadMedia()
})

async function loadMedia() {
  try {
    isLoading.value = true
    const data = await getAllMedia({ limit: 50 })
    mediaList.value = data.items
  } catch (error: any) {
    message.value = 'Failed to load media'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleCreateMedia() {
  try {
    isLoading.value = true
    await createMedia(createForm.value)
    message.value = 'Media created successfully!'
    messageType.value = 'success'
    showCreateForm.value = false
    createForm.value = {
      media_type: 'movie' as any,
      title: '',
      synopsis: '',
      release_date: ''
    }
    await loadMedia()
  } catch (error: any) {
    message.value = error.message || 'Failed to create media'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleUpdateMedia() {
  if (!editingMedia.value) return
  try {
    isLoading.value = true
    await updateMedia(editingMedia.value.id, {
      title: editingMedia.value.title,
      synopsis: editingMedia.value.synopsis
    })
    message.value = 'Media updated successfully!'
    messageType.value = 'success'
    editingMedia.value = null
    await loadMedia()
  } catch (error: any) {
    message.value = error.message || 'Failed to update media'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleDeleteMedia(id: string) {
  if (!confirm('Are you sure you want to delete this media?')) return
  try {
    isLoading.value = true
    await deleteMedia(id)
    message.value = 'Media deleted successfully!'
    messageType.value = 'success'
    await loadMedia()
  } catch (error: any) {
    message.value = error.message || 'Failed to delete media'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

const filteredMedia = computed(() => {
  if (!searchQuery.value) return mediaList.value
  const query = searchQuery.value.toLowerCase()
  return mediaList.value.filter(media =>
    media.title.toLowerCase().includes(query)
  )
})
</script>

<template>
  <div class="media-admin max-w-6xl mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Media Management</h1>
      <button
        @click="showCreateForm = !showCreateForm"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        {{ showCreateForm ? 'Cancel' : 'Add New Media' }}
      </button>
    </div>

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

    <!-- Search -->
    <div class="mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search media..."
        class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Create Form -->
    <div v-if="showCreateForm" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">Create New Media</h2>
      <form @submit.prevent="handleCreateMedia" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Media Type</label>
          <select
            v-model="createForm.media_type"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="movie">Movie</option>
            <option value="tv_series">TV Series</option>
            <option value="video_game">Video Game</option>
            <option value="book">Book</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Title</label>
          <input
            v-model="createForm.title"
            type="text"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Synopsis</label>
          <textarea
            v-model="createForm.synopsis"
            rows="3"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Release Date</label>
          <input
            v-model="createForm.release_date"
            type="date"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          :disabled="isLoading"
          class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {{ isLoading ? 'Creating...' : 'Create Media' }}
        </button>
      </form>
    </div>

    <!-- Media List -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-900">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Title</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Type</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Rating</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="media in filteredMedia" :key="media.id">
            <td class="px-6 py-4 whitespace-nowrap">{{ media.title }}</td>
            <td class="px-6 py-4 whitespace-nowrap capitalize">{{ media.media_type }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ media.average_rating.toFixed(1) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button
                @click="editingMedia = media"
                class="text-blue-600 hover:text-blue-900 mr-3"
              >
                Edit
              </button>
              <button
                @click="handleDeleteMedia(media.id)"
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingMedia" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 max-w-md w-full">
        <h2 class="text-xl font-semibold mb-4">Edit Media</h2>
        <form @submit.prevent="handleUpdateMedia" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Title</label>
            <input
              v-model="editingMedia.title"
              type="text"
              required
              class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Synopsis</label>
            <textarea
              v-model="editingMedia.synopsis"
              rows="3"
              class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>
          <div class="flex space-x-3">
            <button
              type="submit"
              :disabled="isLoading"
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
            >
              {{ isLoading ? 'Saving...' : 'Save Changes' }}
            </button>
            <button
              type="button"
              @click="editingMedia = null"
              class="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>