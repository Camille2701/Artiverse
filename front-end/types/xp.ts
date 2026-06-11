export interface XPProgress {
  current_level: number
  current_xp: number
  xp_in_current_level: number
  xp_needed_for_next_level: number
  progress_percentage: number
  next_level: number
}

export interface LeaderboardEntry {
  username: string
  avatar_url: string | null
  level: number
  experience_points: number
  rank: number
}