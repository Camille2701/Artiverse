import type { Review, ReviewCreate, ReviewUpdate } from '~/types/review'

export const useReviews = () => {
  const { fetchWithAuth } = useApi()

  async function createReview(review: ReviewCreate): Promise<Review> {
    return await fetchWithAuth<Review>('/api/v1/reviews', {
      method: 'POST',
      body: review
    })
  }

  async function getReviewById(id: string): Promise<Review> {
    return await $fetch<Review>(`/api/v1/reviews/${id}`)
  }

  async function getReviewsByMedia(mediaId: string, params?: { skip?: number; limit?: number }): Promise<{
    items: Review[]
    total: number
  }> {
    const queryString = new URLSearchParams(params as any).toString()
    const url = queryString ? `/api/v1/reviews/media/${mediaId}?${queryString}` : `/api/v1/reviews/media/${mediaId}`
    return await $fetch(url)
  }

  async function getReviewsByUser(userId: string, params?: { skip?: number; limit?: number }): Promise<{
    items: Review[]
    total: number
  }> {
    const queryString = new URLSearchParams(params as any).toString()
    const url = queryString ? `/api/v1/reviews/user/${userId}?${queryString}` : `/api/v1/reviews/user/${userId}`
    return await $fetch(url)
  }

  async function updateReview(id: string, review: ReviewUpdate): Promise<Review> {
    return await fetchWithAuth<Review>(`/api/v1/reviews/${id}`, {
      method: 'PUT',
      body: review
    })
  }

  async function deleteReview(id: string): Promise<void> {
    await fetchWithAuth(`/api/v1/reviews/${id}`, {
      method: 'DELETE'
    })
  }

  async function likeReview(id: string): Promise<Review> {
    return await fetchWithAuth<Review>(`/api/v1/reviews/${id}/like`, {
      method: 'POST'
    })
  }

  return {
    createReview,
    getReviewById,
    getReviewsByMedia,
    getReviewsByUser,
    updateReview,
    deleteReview,
    likeReview
  }
}