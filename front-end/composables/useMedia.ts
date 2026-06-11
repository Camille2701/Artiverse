import type { Media, MediaCreate, MediaUpdate } from '~/types/media'

export const useMedia = () => {
  const { fetchWithAuth } = useApi()

  async function getAllMedia(params?: { skip?: number; limit?: number; media_type?: string | null; sort_by?: string; order?: string }): Promise<{
    items: Media[]
    total: number
  }> {
    const cleaned: Record<string, string> = {}
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        if (v != null) cleaned[k] = String(v)
      }
    }
    const queryString = new URLSearchParams(cleaned).toString()
    const url = queryString ? `/api/v1/media?${queryString}` : '/api/v1/media'
    return await $fetch(url)
  }

  async function getMediaById(id: string): Promise<Media> {
    return await $fetch<Media>(`/api/v1/media/${id}`)
  }

  async function searchMedia(query: string, params?: any): Promise<{
    items: Media[]
    total: number
  }> {
    const queryString = new URLSearchParams({ query, ...params }).toString()
    return await $fetch(`/api/v1/media/search?${queryString}`)
  }

  async function getTrendingMedia(params?: { skip?: number; limit?: number; media_type?: string | null }): Promise<Media[]> {
    const cleaned: Record<string, string> = {}
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        if (v != null) cleaned[k] = String(v)
      }
    }
    const queryString = new URLSearchParams(cleaned).toString()
    const url = queryString ? `/api/v1/media/trending?${queryString}` : '/api/v1/media/trending'
    const response = await $fetch<{ items: Media[]; total: number } | Media[]>(url)
    // Backend returns { items, total } shape
    if (response && !Array.isArray(response) && 'items' in response) {
      return response.items
    }
    return response as Media[]
  }

  async function createMedia(media: MediaCreate): Promise<Media> {
    return await fetchWithAuth<Media>('/api/v1/media', {
      method: 'POST',
      body: media
    })
  }

  async function updateMedia(id: string, media: MediaUpdate): Promise<Media> {
    return await fetchWithAuth<Media>(`/api/v1/media/${id}`, {
      method: 'PUT',
      body: media
    })
  }

  async function deleteMedia(id: string): Promise<void> {
    await fetchWithAuth(`/api/v1/media/${id}`, {
      method: 'DELETE'
    })
  }

  async function getSuggestions(id: string, limit = 8): Promise<{
    items: Media[]
    total: number
  }> {
    return await $fetch(`/api/v1/media/${id}/suggestions?limit=${limit}`)
  }

  return {
    getAllMedia,
    getMediaById,
    searchMedia,
    getTrendingMedia,
    getSuggestions,
    createMedia,
    updateMedia,
    deleteMedia
  }
}