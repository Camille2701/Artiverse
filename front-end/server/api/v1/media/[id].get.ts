export default defineEventHandler(async (event) => {
  try {
    const id = getRouterParam(event, 'id')
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';

    const response = await $fetch(`${backendUrl}/api/v1/media/${id}`, {
      headers: {
        'Authorization': `Bearer ${getCookie(event, 'auth_token') || ''}`
      }
    });

    return response;
  } catch (error: any) {
    console.error('Failed to fetch media:', error);
    throw createError({
      statusCode: error.statusCode || 404,
      statusMessage: error.data?.detail || 'Media not found'
    });
  }
})