export type User = {
  id: string
  username: string
  email: string
  bio: string | null
  avatar_url: string | null
  level: number
  experience_points: number
  streak_days: number
  last_login_date: string | null
  created_at: string
  updated_at: string
}

export type UserUpdate = Partial<Pick<User, 'username' | 'bio' | 'avatar_url'>>

export type PasswordUpdate = {
  current_password: string
  new_password: string
}

export type Follow = {
  id: string
  follower_id: string
  followed_id: string
  created_at: string
}

export type ActivityLog = {
  id: string
  user_id: string
  activity_type: string
  entity_type: string | null
  entity_id: string | null
  activity_metadata: any
  created_at: string
}