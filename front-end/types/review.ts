export type Review = {
  id: string
  title: string
  content: string
  spoiler: boolean
  user_id: string
  media_id: string
  like_count: number
  created_at: string
  updated_at: string
}

export type ReviewCreate = {
  title: string
  content: string
  spoiler?: boolean
  media_id: string
}

export type ReviewUpdate = {
  title?: string
  content?: string
  spoiler?: boolean
}