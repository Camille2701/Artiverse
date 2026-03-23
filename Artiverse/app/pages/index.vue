<template>
  <div>
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
      <h2 class="text-3xl font-extrabold text-gray-900">Bibliothèque Multimédia</h2>
      <button 
        @click="showForm = !showForm" 
        class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gray-900"
      >
        {{ showForm ? 'Annuler' : 'Ajouter un média' }}
      </button>
    </div>

    <div v-if="showForm" class="mb-8">
        <MediaForm @submit="handleAdd" />
    </div>
    
    <div>

      <div class="space-y-6">
        <div v-if="pending" class="flex justify-center items-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>

        <div v-else-if="error" class="bg-red-50 p-4 rounded-md">
           <h3 class="text-lg font-medium text-red-800">Erreur de chargement</h3>
           <p class="text-sm text-red-700 mt-2">{{ error.message }}</p>
           <button @click="refresh()" class="mt-4 text-sm font-medium text-red-600 hover:text-red-500">Réessayer</button>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <MediaCard 
            v-for="media in mediaList" 
            :key="media.id" 
            :media="media"
            @select="handleSelect"
            @delete="handleDelete"
          >
             <template #actions>

                  <button class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded transition">
                    Modifier
                  </button>
             </template>
          </MediaCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Media } from '~~/types/media';

definePageMeta({
  layout: 'content'
});


const showForm = ref(false);
const { data: mediaList, pending, error, refresh } = await useFetch<Media[]>('/api/media');

function handleSelect(media: Media) {

  console.log('Selected media:', media.title);

}

function handleDelete(id: string) {
  if (!mediaList.value) return;
  
  if (confirm('Êtes-vous sûr de vouloir supprimer ce média ?')) {
     mediaList.value = mediaList.value.filter(m => m.id !== id);
  }
}

async function handleAdd(formData: any) {

  console.log('Adding media:', formData);
  

  try {
      const { data } = await useFetch('/api/media', {
          method: 'POST',
          body: formData
      });
      
      if (data.value && (data.value as any).success) {

           if (mediaList.value) {
               mediaList.value.push((data.value as any).media);
           }
      }
  } catch (e) {
      console.error('Failed to add media', e);
  }
}
</script>
