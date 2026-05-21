export interface UserStatistics {
  user_id: string
  total_reviews: number
  total_ratings: number
  total_lists: number
  total_media_in_lists: number
  total_interactions: number
  reviews_by_type: Record<string, number>
  ratings_by_type: Record<string, { count: number; average_score: number }>
  activity_timeline: Record<string, number>
  top_rated: Array<{
    media_id: string
    title: string
    media_type: string
    cover_image?: string
    rating: number
  }>
  taste_distribution: Record<string, { total: number; percentage: number }>
  generated_at: string
}

export interface PlatformStatistics {
  total_users: number
  total_media: number
  total_reviews: number
  total_ratings: number
  total_lists: number
  media_by_type: Record<string, number>
  most_active_users: Array<{
    user_id: string
    username: string
    total_activity: number
    reviews: number
    ratings: number
  }>
  generated_at: string
}