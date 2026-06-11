export interface Rating {
  id: string
  user_id: string
  media_id: string
  score: number
  created_at: string
  updated_at: string
}

export interface RatingCreate {
  media_id: string
  score: number
}