<template>
  <div class="glass rounded-xl p-6 border border-white/10">
    <h3 class="text-lg font-display font-semibold text-text-primary mb-4">Répartition médias</h3>

    <div class="relative w-full aspect-square max-w-xs mx-auto">
      <!-- SVG Radar Chart -->
      <svg viewBox="0 0 200 200" class="w-full h-full">
        <!-- Background grid -->
        <polygon
          v-for="level in [25, 50, 75, 100]"
          :key="level"
          :points="getPolygonPoints(level)"
          fill="none"
          :stroke="level === 100 ? '#2A2A38' : '#1E1E28'"
          stroke-width="1"
        />

        <!-- Axis lines -->
        <line
          v-for="(axis, index) in axes"
          :key="index"
          :x1="100"
          :y1="100"
          :x2="getAxisPoint(axis.angle, 100).x"
          :y2="getAxisPoint(axis.angle, 100).y"
          stroke="#2A2A38"
          stroke-width="1"
        />

        <!-- Data polygon -->
        <polygon
          :points="getDataPoints()"
          :fill="gradientId"
          fill-opacity="0.3"
          stroke="url(#gradientStroke)"
          stroke-width="2"
        />

        <!-- Data points -->
        <circle
          v-for="(axis, index) in axes"
          :key="`point-${index}`"
          :cx="getAxisPoint(axis.angle, axis.value).x"
          :cy="getAxisPoint(axis.angle, axis.value).y"
          r="4"
          :fill="axis.color"
          class="hover:scale-150 transition-transform cursor-pointer"
        />

        <!-- Gradients -->
        <defs>
          <linearGradient :id="gradientId" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FF4757" stop-opacity="0.8" />
            <stop offset="50%" stop-color="#9B51E0" stop-opacity="0.8" />
            <stop offset="100%" stop-color="#00D2D3" stop-opacity="0.8" />
          </linearGradient>
          <linearGradient id="gradientStroke" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FF4757" />
            <stop offset="50%" stop-color="#9B51E0" />
            <stop offset="100%" stop-color="#00D2D3" />
          </linearGradient>
        </defs>
      </svg>

      <!-- Labels -->
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="text-center">
          <p class="text-3xl font-display font-bold text-text-primary">{{ totalItems }}</p>
          <p class="text-text-secondary text-xs">Total</p>
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div class="grid grid-cols-2 gap-3 mt-6">
      <div
        v-for="axis in axes"
        :key="axis.label"
        class="flex items-center gap-2"
      >
        <div
          class="w-3 h-3 rounded-full"
          :style="{ backgroundColor: axis.color }"
        />
        <div class="flex-1">
          <div class="flex justify-between text-sm">
            <span class="text-text-secondary">{{ axis.label }}</span>
            <span class="text-text-primary font-medium">{{ axis.value }}%</span>
          </div>
          <div class="h-1 bg-bg-tertiary rounded-full mt-1">
            <div
              class="h-full rounded-full transition-all duration-500"
              :style="{
                width: `${axis.value}%`,
                backgroundColor: axis.color
              }"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface MediaStats {
  movies: number
  series: number
  games: number
  books: number
}

interface Props {
  stats: MediaStats
}

const props = defineProps<Props>()

const gradientId = 'radarGradient'

const totalItems = computed(() => {
  return props.stats.movies + props.stats.series + props.stats.games + props.stats.books
})

const axes = computed(() => {
  const total = totalItems.value || 1 // Avoid division by zero

  return [
    {
      label: 'Films',
      value: Math.round((props.stats.movies / total) * 100),
      angle: 0, // Top
      color: '#FF4757'
    },
    {
      label: 'Séries',
      value: Math.round((props.stats.series / total) * 100),
      angle: 90, // Right
      color: '#9B51E0'
    },
    {
      label: 'Jeux',
      value: Math.round((props.stats.games / total) * 100),
      angle: 180, // Bottom
      color: '#00D2D3'
    },
    {
      label: 'Livres',
      value: Math.round((props.stats.books / total) * 100),
      angle: 270, // Left
      color: '#ECCC68'
    }
  ]
})

function getPolygonPoints(radius: number): string {
  return axes.value
    .map(axis => {
      const point = getAxisPoint(axis.angle, radius)
      return `${point.x},${point.y}`
    })
    .join(' ')
}

function getDataPoints(): string {
  return axes.value
    .map(axis => {
      const point = getAxisPoint(axis.angle, axis.value)
      return `${point.x},${point.y}`
    })
    .join(' ')
}

function getAxisPoint(angle: number, radius: number): { x: number, y: number } {
  const radians = (angle - 90) * (Math.PI / 180)
  return {
    x: 100 + radius * Math.cos(radians),
    y: 100 + radius * Math.sin(radians)
  }
}
</script>