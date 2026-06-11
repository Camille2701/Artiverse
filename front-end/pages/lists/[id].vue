<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useLists } from '~/composables/useLists'
import { useMedia } from '~/composables/useMedia'
import type { MediaList, Media } from '~/types/media'

const { getListById, addMediaToList, removeMediaFromList } = useLists()
const { getAllMedia } = useMedia()

const list = ref<MediaList | null>(null)
const allMedia = ref<Media[]>([])
const isLoading = ref(false)
const showAddMedia = ref(false)
const selectedMedia = ref('')
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

const route = useRoute()

onMounted(async () => {
  await loadList()
  await loadMedia()
})

async function loadList() {
  try {
    isLoading.value = true
    list.value = await getListById(route.params.id as string)
  } catch (error: any) {
    message.value = 'Failed to load list'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function loadMedia() {
  try {
    const result = await getAllMedia({ limit: 100 })
    allMedia.value = result.items
  } catch (error: any) {
    console.error('Failed to load media:', error)
  }
}

async function handleAddMedia() {
  if (!selectedMedia.value) return
  try {
    isLoading.value = true
    await addMediaToList(route.params.id as string, selectedMedia.value)
    message.value = 'Media added to list!'
    messageType.value = 'success'
    showAddMedia.value = false
    selectedMedia.value = ''
    await loadList()
  } catch (error: any) {
    message.value = error.message || 'Failed to add media to list'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

async function handleRemoveMedia(mediaId: string) {
  if (!confirm('Remove this media from the list?')) return
  try {
    isLoading.value = true
    await removeMediaFromList(route.params.id as string, mediaId)
    message.value = 'Media removed from list'
    messageType.value = 'success'
    await loadList()
  } catch (error: any) {
    message.value = error.message || 'Failed to remove media'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

const availableMedia = computed(() => {
  if (!list.value) return allMedia.value
  const listMediaIds = list.value.items?.map(item => item.media_id) || []
  return allMedia.value.filter(media => !listMediaIds.includes(media.id))
})
</script>

<template>
  <div class="list-detail max-w-6xl mx-auto p-6">
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

    <div v-if="list">
      <!-- List Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold">{{ list.name }}</h1>
          <span class="px-2 py-1 rounded text-sm bg-gray-200 dark:bg-gray-700">
            {{ list.visibility }}
          </span>
        </div>
        <button
          @click="showAddMedia = !showAddMedia"
          class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          {{ showAddMedia ? 'Cancel' : 'Add Media' }}
        </button>
      </div>

      <!-- Add Media Form -->
      <div v-if="showAddMedia" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Add Media to List</h2>
        <form @submit.prevent="handleAddMedia" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Select Media</label>
            <select
              v-model="selectedMedia"
              required
              class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Choose a media item...</option>
              <option
                v-for="media in availableMedia"
                :key="media.id"
                :value="media.id"
              >
                {{ media.title }} ({{ media.media_type }})
              </option>
            </select>
          </div>
          <button
            type="submit"
            :disabled="isLoading"
            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {{ isLoading ? 'Adding...' : 'Add to List' }}
          </button>
        </form>
      </div>

      <!-- List Items -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div class="p-6 border-b dark:border-gray-700">
          <h2 class="text-xl font-semibold">
            List Items ({{ list.items?.length || 0 }})
          </h2>
        </div>
        <div v-if="list.items && list.items.length > 0" class="divide-y dark:divide-gray-700">
          <div
            v-for="item in list.items"
            :key="item.id"
            class="p-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            <div class="flex-1">
              <p class="font-medium">{{ item.media_id }}</p>
              <p class="text-sm text-gray-600">Added: {{ new Date(item.created_at).toLocaleDateString() }}</p>
            </div>
            <button
              @click="handleRemoveMedia(item.media_id)"
              class="text-red-600 hover:text-red-900"
            >
              Remove
            </button>
          </div>
        </div>
        <div v-else class="p-6 text-center text-gray-500">
          <p>No media in this list yet. Add some!</p>
        </div>
      </div>
    </div>

    <div v-else-if="!isLoading" class="text-center py-8">
      <p class="text-gray-500">List not found</p>
    </div>
  </div>
</template>