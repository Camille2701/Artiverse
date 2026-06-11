import type { Rating, RatingCreate } from '~/types/rating'

export const useRatings = () => {
  const { fetchWithAuth } = useApi()

  async function createRating(rating: RatingCreate): Promise<Rating> {
    return await fetchWithAuth<Rating>('/api/v1/ratings', {
      method: 'POST',
      body: rating
    })
  }

  async function getRating(mediaId: string): Promise<Rating | null> {
    try {
      return await $fetch<Rating>(`/api/v1/ratings/media/${mediaId}`)
    } catch (error) {
      return null
    }
  }

  async function getUserRatings(params?: { skip?: number; limit?: number }): Promise<{
    items: Rating[]
    total: number
  }> {
    const queryString = new URLSearchParams(params as any).toString()
    const url = queryString ? `/api/v1/ratings?${queryString}` : '/api/v1/ratings'
    return await fetchWithAuth(url)
  }

  async function updateRating(rating: RatingCreate): Promise<Rating> {
    return await fetchWithAuth<Rating>('/api/v1/ratings', {
      method: 'PUT',
      body: rating
    })
  }

  async function deleteRating(ratingId: string): Promise<void> {
    await fetchWithAuth(`/api/v1/ratings/${ratingId}`, {
      method: 'DELETE'
    })
  }

  return {
    createRating,
    getRating,
    getUserRatings,
    updateRating,
    deleteRating
  }
}