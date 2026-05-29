<template>
  <div class="flex items-center gap-2">
    <img
      :src="logoSrc"
      :alt="'Artiverse Logo'"
      :class="logoClass"
    />
    <span v-if="showText" class="text-2xl font-bold text-accent">
      Artiverse
    </span>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  showText?: boolean;
  size?: 'small' | 'medium' | 'large';
}>();

const { isDark } = useTheme();

const logoSrc = computed(() => {
  return isDark.value
    ? '/logos/small_white_bg.png'
    : '/logos/small.png';
});

const logoClass = computed(() => {
  const sizeClasses = {
    small: 'h-6 w-auto',
    medium: 'h-8 w-auto',
    large: 'h-12 w-auto'
  };
  return sizeClasses[props.size || 'medium'];
});
</script>