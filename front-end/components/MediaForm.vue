<template>
  <form @submit.prevent="submit" class="glass p-6 rounded-xl border border-white/10">
    <h3 class="text-xl font-display font-bold mb-6 text-text-primary flex items-center gap-2">
      <UIIcon name="plus" size="medium" />
      Ajouter un média
    </h3>
    <div class="space-y-5">
      <div>
        <label for="title" class="block text-sm font-medium text-text-primary mb-2 font-display">Titre</label>
        <input
          id="title"
          v-model.trim="form.title"
          type="text"
          required
          class="input-field"
          placeholder="Titre du média"
        />
      </div>

      <div>
        <label for="type" class="block text-sm font-medium text-text-primary mb-2 font-display">Type</label>
        <select
          id="type"
          v-model="form.type"
          class="input-field cursor-pointer"
        >
          <option value="Movie">Film</option>
          <option value="Serie">Série</option>
          <option value="Game">Jeu Vidéo</option>
          <option value="Book">Livre</option>
        </select>
      </div>

      <div>
        <label for="description" class="block text-sm font-medium text-text-primary mb-2 font-display">Description</label>
        <textarea
          id="description"
          v-model="form.description"
          rows="3"
          class="input-field resize-none"
          placeholder="Courte description..."
        ></textarea>
      </div>

      <div class="pt-2">
        <button type="submit" class="btn-primary w-full">
          <span class="flex items-center justify-center gap-2">
            <UIIcon name="plus" size="small" />
            Ajouter
          </span>
        </button>
      </div>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { MediaType } from '~/types/media';
import UIIcon from '~/components/icons/UIIcon.vue';

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
