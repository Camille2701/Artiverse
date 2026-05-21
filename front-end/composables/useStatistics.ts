import type { UserStatistics, PlatformStatistics } from '~/types/statistics'

export const useStatistics = () => {
  const { isAuthenticated } = useAuth()

  async function getMyStatistics(): Promise<UserStatistics> {
    if (!isAuthenticated.value) {
      throw new Error('User must be authenticated')
    }

    return await $fetch<UserStatistics>('/api/v1/statistics/me')
  }

  async function getUserStatistics(userId: string): Promise<UserStatistics> {
    return await $fetch<UserStatistics>(`/api/v1/statistics/users/${userId}`)
  }

  async function getPlatformStatistics(): Promise<PlatformStatistics> {
    return await $fetch<PlatformStatistics>('/api/v1/statistics/platform')
  }

  async function compareUsers(compareUserId: string): Promise<any> {
    if (!isAuthenticated.value) {
      throw new Error('User must be authenticated')
    }

    return await $fetch(`/api/v1/statistics/compare/${compareUserId}`)
  }

  async function getActivityLeaderboard(limit: number = 10): Promise<any> {
    return await $fetch(`/api/v1/statistics/leaderboard?limit=${limit}`)
  }

  return {
    getMyStatistics,
    getUserStatistics,
    getPlatformStatistics,
    compareUsers,
    getActivityLeaderboard
  }
}