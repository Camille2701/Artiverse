import type { Media } from '~~/types/media';

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id');

  if (!id) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Media ID is required'
    });
  }

  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const response = await $fetch(`${backendUrl}/api/v1/media/${id}`);

    // Transform backend response to frontend format
    return {
      id: response.id,
      title: response.title,
      type: response.media_type,
      description: response.synopsis,
      rating: response.average_rating,
      releaseDate: response.release_date,
      image: response.cover_image
    };
  } catch (error: any) {
    console.error('Failed to fetch media from backend:', error);

    throw createError({
      statusCode: error.statusCode || 404,
      statusMessage: error.data?.detail || 'Media not found'
    });
  }
});