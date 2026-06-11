<script setup lang="ts">
useHead({
  title: 'Artiverse - Classement',
  meta: [{ name: 'description', content: 'Classement des membres les plus actifs' }]
})

const { user: currentUser } = useAuth()

const leaderboard = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const data = await $fetch<{ leaderboard: any[] }>('/api/v1/xp/leaderboard?limit=20')
    leaderboard.value = data.leaderboard ?? []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

function levelColor(level: number): string {
  if (level >= 10) return '#f59e0b'
  if (level >= 7) return '#a855f7'
  if (level >= 4) return '#3b82f6'
  return '#22c55e'
}

function rankStyle(rank: number): string {
  if (rank === 1) return 'background: linear-gradient(135deg, #f59e0b, #fbbf24); color: #1a1a1a'
  if (rank === 2) return 'background: linear-gradient(135deg, #94a3b8, #cbd5e1); color: #1a1a1a'
  if (rank === 3) return 'background: linear-gradient(135deg, #cd7f32, #b45309); color: #fff'
  return 'background: rgba(255,255,255,0.06); color: var(--color-text-secondary)'
}

function rankEmoji(rank: number): string {
  if (rank === 1) return '🥇'
  if (rank === 2) return '🥈'
  if (rank === 3) return '🥉'
  return `#${rank}`
}
</script>

<template>
  <div class="mx-auto my-4 w-full max-w-3xl px-4 py-4 sm:my-8">
    <!-- Header -->
    <div class="glass rounded-2xl p-6 border border-white/10 mb-8 text-center">
      <div class="text-5xl mb-3">🏆</div>
      <h1 class="text-3xl font-bold text-text-primary font-display mb-2">Classement</h1>
      <p class="text-text-secondary font-body">Les membres les plus actifs d'Artiverse</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-16">
      <div class="spinner !h-10 !w-10 !border-4"></div>
    </div>

    <!-- Leaderboard list -->
    <div v-else class="space-y-3">
      <div
        v-for="entry in leaderboard"
        :key="entry.username"
        class="glass rounded-xl border transition-all duration-200"
        :class="[
          entry.username === currentUser?.username
            ? 'border-accent/60 shadow-lg shadow-accent/10'
            : 'border-border-color hover:border-white/20'
        ]"
      >
        <div class="flex items-center gap-4 p-4">
          <!-- Rank badge -->
          <div
            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-sm font-extrabold font-display"
            :style="rankStyle(entry.rank)"
          >
            {{ entry.rank <= 3 ? rankEmoji(entry.rank) : `#${entry.rank}` }}
          </div>

          <!-- Avatar -->
          <img
            :src="entry.avatar_url || 'https://i.pravatar.cc/80?u=' + entry.username"
            :alt="entry.username"
            class="h-11 w-11 rounded-full object-cover border-2 border-bg-tertiary shrink-0"
          />

          <!-- Name + level -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="font-semibold text-text-primary font-display truncate">{{ entry.username }}</span>
              <span v-if="entry.username === currentUser?.username" class="text-xs bg-accent/20 text-accent rounded-full px-2 py-0.5 font-semibold">Vous</span>
            </div>
            <div class="text-xs text-text-tertiary font-body mt-0.5">
              Niveau {{ entry.level }} · {{ entry.experience_points }} XP
            </div>
          </div>

          <!-- Level pill -->
          <div
            class="shrink-0 rounded-full px-3 py-1.5 text-xs font-bold font-display"
            :style="{ background: levelColor(entry.level) + '22', color: levelColor(entry.level), border: `1px solid ${levelColor(entry.level)}44` }"
          >
            Niv. {{ entry.level }}
          </div>

          <!-- XP bar -->
          <div class="hidden sm:flex flex-col items-end gap-1 w-28 shrink-0">
            <span class="text-xs text-text-tertiary font-body">{{ entry.experience_points }} XP</span>
            <div class="h-1.5 w-full rounded-full overflow-hidden" style="background: rgba(255,255,255,0.08)">
              <div
                class="h-full rounded-full"
                :style="{
                  background: `linear-gradient(90deg, ${levelColor(entry.level)}, ${levelColor(entry.level)}aa)`,
                  width: Math.min(100, Math.max(4,
                    ((entry.experience_points - 100 * Math.max(0, entry.level - 1) ** 2) /
                     (100 * entry.level ** 2 - 100 * Math.max(0, entry.level - 1) ** 2)) * 100
                  )) + '%'
                }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="leaderboard.length === 0" class="glass rounded-xl p-10 border border-border-color text-center">
        <div class="text-4xl mb-4">😶</div>
        <p class="text-text-secondary font-body">Aucun utilisateur pour l'instant.</p>
      </div>
    </div>
  </div>
</template>
