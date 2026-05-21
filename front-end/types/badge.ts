export enum BadgeTier {
  Flat = 'flat',
  Gradient = 'gradient',
  Holographic = 'holographic'
}

export enum BadgeCategory {
  GenreExpert = 'genre_expert',
  Achievement = 'achievement',
  Social = 'social',
  Rare = 'rare'
}

export interface Badge {
  id: string
  name: string
  description: string
  icon?: string
  tier: BadgeTier
  category: BadgeCategory
  requirements?: any
  xp_reward: number
}

export interface UserBadge {
  id: string
  name: string
  description: string
  icon?: string
  tier: BadgeTier
  category: BadgeCategory
  earned_at?: string
  is_equipped: boolean
  progress?: any
  xp_reward: number
}

export interface BadgeProgress {
  badge_name: string
  current: number
  target: number
  percentage: number
  is_complete: boolean
}