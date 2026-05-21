import type { Review } from '~~/types/review'

export default defineEventHandler(async (event) => {
  try {
    const id = getRouterParam(event, 'id')
    const query = getQuery(event)

    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const skip = query.skip ? parseInt(query.skip as string) : 0
    const limit = query.limit ? parseInt(query.limit as string) : 10

    const response = await $fetch<{
      items: Review[]
      total: number
      skip: number
      limit: number
    }>(`${backendUrl}/api/v1/users/${id}/reviews`, {
      params: { skip, limit },
      headers: {
        'Authorization': `Bearer ${getCookie(event, 'auth_token') || ''}`
      }
    });

    return response;
  } catch (error: any) {
    console.error('Failed to fetch user reviews from backend:', error);

    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.data?.detail || 'Failed to fetch reviews'
    });
  }
})