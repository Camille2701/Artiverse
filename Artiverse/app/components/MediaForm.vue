<template>
  <form @submit.prevent="submit" class="bg-white p-6 rounded-lg shadow-md border border-gray-200">
    <h3 class="text-lg font-semibold mb-4 text-gray-800">Ajouter un média</h3>
    <div class="space-y-4">
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Titre</label>
        <input 
          id="title"
          v-model.trim="form.title" 
          type="text" 
          required
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" 
          placeholder="Titre du média"
        />
      </div>
      
      <div>
        <label for="type" class="block text-sm font-medium text-gray-700 mb-1">Type</label>
        <select 
          id="type"
          v-model="form.type"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
        >
          <option value="Movie">Film</option>
          <option value="Game">Jeu Vidéo</option>
          <option value="Book">Livre</option>
        </select>
      </div>

      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
        <textarea 
          id="description"
          v-model="form.description" 
          rows="3"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          placeholder="Courte description..."
        ></textarea>
      </div>

      <div class="pt-2">
        <button type="submit" class="btn-accent">
          Ajouter
        </button>
      </div>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { MediaType } from '~~/types/media';

const emit = defineEmits(['submit']);

const form = reactive({
  title: '',
  type: MediaType.Movie,
  description: ''
});

function submit() {
  if (!form.title) return;
  
  emit('submit', { ...form });
  
  // Reset form basics
  form.title = '';
  form.description = '';
  form.type = MediaType.Movie;
}
</script>
