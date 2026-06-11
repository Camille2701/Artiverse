export enum MediaType {
  Movie = 'movie',
  Game = 'video_game',
  Book = 'book',
  Serie = 'tv_series'
}

export interface Media {
  id: string
  title: string
  media_type: MediaType
  original_title?: string
  synopsis?: string
  release_date?: string
  cover_image?: string
  banner_image?: string
  average_rating: number
  popularity_score: number
  created_at: string
  updated_at: string
}

export interface MediaCreate {
  media_type: MediaType
  title: string
  original_title?: string
  synopsis?: string
  release_date?: string
}

export interface MediaUpdate {
  title?: string
  original_title?: string
  synopsis?: string
  release_date?: string
  cover_image?: string
  banner_image?: string
}
