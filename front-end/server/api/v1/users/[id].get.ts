import type { User } from '~~/types/user'

export default defineEventHandler(async (event) => {
  try {
    const id = getRouterParam(event, 'id')

    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const response = await $fetch<User>(`${backendUrl}/api/v1/users/${id}`, {
      headers: {
        'Authorization': `Bearer ${getCookie(event, 'auth_token') || ''}`
      }
    });

    return response;
  } catch (error: any) {
    console.error('Failed to fetch user from backend:', error);

    throw createError({
      statusCode: error.statusCode || 404,
      statusMessage: error.data?.detail || 'User not found'
    });
  }
})