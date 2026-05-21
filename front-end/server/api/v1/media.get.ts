export default defineEventHandler(async (event) => {
  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const query = getQuery(event);

    const params: Record<string, string> = {};
    if (query.media_type) params.media_type = query.media_type as string;
    if (query.year) params.year = query.year as string;
    if (query.genre) params.genre = query.genre as string;
    if (query.skip) params.skip = query.skip as string;
    if (query.limit) params.limit = query.limit as string;

    const response = await $fetch(`${backendUrl}/api/v1/media`, {
      params,
      headers: {
        'Authorization': `Bearer ${getCookie(event, 'auth_token') || ''}`
      }
    });

    return response;
  } catch (error) {
    console.error('Failed to fetch media from backend:', error);
    return [];
  }
})