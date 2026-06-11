<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<style src="~/assets/css/artiverse-vars.css"></style>
<style src="~/assets/css/artiverse.css"></style>

<script setup>
import { onErrorCaptured } from 'vue'

onErrorCaptured((err, instance, info) => {
  console.log('Composant source :', instance?.$options?.__file)
  console.log('Info :', info)
  console.error(err)
  return false
})
</script>