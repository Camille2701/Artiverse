export type MediaType = 'film' | 'serie' | 'jeu' | 'livre'

export interface User {
  id: number
  username: string
  createdAt: Date
}


export interface MediaItem {
  id: number
  title: string
  imgLink: string
  imgAlt: string
  year: number
  type: MediaType
  score: number
  tags: string[]
  nbcritiques? : number
  critiques: number
  rank?: number
  description?: string
  duration?: string
  director?: string
  author?: string
}

export interface Critique {
  id: number
  user: User
  note?: number
  commentaire: string
  date: Date
}

export interface SideItem {
    id: number
    title: string
    score: number
    imgLink: string
    imgAlt: string
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
  imgLink: string
  imgLabel: string
}

export interface StatItem {
    imgLink: string
    imgAlt: string
    value: string
    label: string
}
