export interface MediaList {
  id: string
  user_id: string
  name: string
  visibility: string
  created_at: string
  updated_at: string
  items?: ListItem[]
}

export interface ListCreate {
  name: string
  visibility?: string
}

export interface ListUpdate {
  name?: string
  visibility?: string
}

export interface ListItem {
  id: string
  list_id: string
  media_id: string
  created_at: string
}