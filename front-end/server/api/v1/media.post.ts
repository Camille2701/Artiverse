export default defineEventHandler(async (event) => {
  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const body = await readBody(event);

    const response = await $fetch(`${backendUrl}/api/v1/media`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getCookie(event, 'auth_token') || ''}`
      },
      body
    });

    return response;
  } catch (error: any) {
    console.error('Failed to create media:', error);
    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.data?.detail || 'Failed to create media'
    });
  }
})