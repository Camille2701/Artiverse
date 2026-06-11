import type { XPProgress, LeaderboardEntry } from '~/types/xp'

export const useXP = () => {
  const { fetchWithAuth } = useApi()

  async function getXPProgress(): Promise<XPProgress> {
    return await fetchWithAuth<XPProgress>('/api/v1/xp/progress')
  }

  async function getLeaderboard(params?: { limit?: number }): Promise<LeaderboardEntry[]> {
    const queryString = new URLSearchParams(params as any).toString()
    const url = queryString ? `/api/v1/xp/leaderboard?${queryString}` : '/api/v1/xp/leaderboard'
    return await $fetch<LeaderboardEntry[]>(url)
  }

  async function claimDailyLogin(): Promise<{ xp_gained: number; new_level: number }> {
    return await fetchWithAuth('/api/v1/xp/daily-login', {
      method: 'POST'
    })
  }

  return {
    getXPProgress,
    getLeaderboard,
    claimDailyLogin
  }
}