export type MediaType = 'film' | 'serie' | 'jeu' | 'livre'

export interface MediaItem {
  id: number
  title: string
  year: number
  type: MediaType
  score: number
  tags: string[]
  rank?: number
  description?: string
  duration?: string
  director?: string
}

export interface ActivityItem {
  id: number
  user: { initials: string; color: string; textColor: string }
  action: string
  target: string
  extra?: string
  extraType?: 'badge' | 'quote'
  time: string
}

export interface CategoryItem {
  id: MediaType
  label: string
  count: string
  icon: string
  iconColor: string
  iconBg: string
}

export interface StatItem {
    imgLink: string
    imgAlt: string
    value: string
    label: string
}
