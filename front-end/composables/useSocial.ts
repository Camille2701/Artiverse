import type { ActivityLog, Follow, User } from '~/types/user'

export const useSocial = () => {
  const { fetchWithAuth } = useApi()

  async function followUser(userId: string): Promise<Follow> {
    return await fetchWithAuth<Follow>(`/api/v1/social/follow/${userId}`, {
      method: 'POST'
    })
  }

  async function unfollowUser(userId: string): Promise<void> {
    await fetchWithAuth(`/api/v1/social/follow/${userId}`, {
      method: 'DELETE'
    })
  }

  async function getFollowers(userId: string): Promise<User[]> {
    return await $fetch<User[]>(`/api/v1/social/followers/${userId}`)
  }

  async function getFollowing(userId: string): Promise<User[]> {
    return await $fetch<User[]>(`/api/v1/social/following/${userId}`)
  }

  async function getActivityFeed(params?: { skip?: number; limit?: number }): Promise<{
    items: ActivityLog[]
    total: number
  }> {
    const queryString = new URLSearchParams(params as any).toString()
    const url = queryString ? `/api/v1/social/feed?${queryString}` : '/api/v1/social/feed'
    return await fetchWithAuth(url)
  }

  async function getUserActivity(userId: string, params?: { skip?: number; limit?: number }): Promise<{
    items: ActivityLog[]
    total: number
  }> {
    const queryString = new URLSearchParams(params as any).toString()
    const url = queryString ? `/api/v1/social/activity/${userId}?${queryString}` : `/api/v1/social/activity/${userId}`
    return await $fetch(url)
  }

  return {
    followUser,
    unfollowUser,
    getFollowers,
    getFollowing,
    getActivityFeed,
    getUserActivity
  }
}