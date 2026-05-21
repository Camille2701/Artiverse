import type { Badge, UserBadge, BadgeProgress } from '~/types/badge'

export const useBadges = () => {
  const { isAuthenticated } = useAuth()

  async function getAvailableBadges(): Promise<Badge[]> {
    return await $fetch<Badge[]>('/api/v1/badges/available')
  }

  async function getMyBadges(): Promise<UserBadge[]> {
    if (!isAuthenticated.value) {
      throw new Error('User must be authenticated')
    }

    return await $fetch<UserBadge[]>('/api/v1/badges/my-badges')
  }

  async function getUserBadges(userId: string): Promise<UserBadge[]> {
    return await $fetch<UserBadge[]>(`/api/v1/badges/users/${userId}`)
  }

  async function checkEligibility(): Promise<{ eligible_badges: Badge[] }> {
    if (!isAuthenticated.value) {
      throw new Error('User must be authenticated')
    }

    return await $fetch('/api/v1/badges/check-eligibility')
  }

  async function awardNewBadges(): Promise<{ awarded_badges: any[], total_awarded: number }> {
    if (!isAuthenticated.value) {
      throw new Error('User must be authenticated')
    }

    return await $fetch('/api/v1/badges/award-new', {
      method: 'POST'
    })
  }

  async function getBadgeProgress(badgeId: string): Promise<BadgeProgress> {
    if (!isAuthenticated.value) {
      throw new Error('User must be authenticated')
    }

    return await $fetch<BadgeProgress>(`/api/v1/badges/progress/${badgeId}`)
  }

  async function equipBadge(badgeId: string): Promise<{ message: string }> {
    if (!isAuthenticated.value) {
      throw new Error('User must be authenticated')
    }

    return await $fetch(`/api/v1/badges/equip/${badgeId}`, {
      method: 'POST'
    })
  }

  return {
    getAvailableBadges,
    getMyBadges,
    getUserBadges,
    checkEligibility,
    awardNewBadges,
    getBadgeProgress,
    equipBadge
  }
}