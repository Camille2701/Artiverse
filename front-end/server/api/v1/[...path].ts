// Catch-all proxy for /api/v1/** -> FastAPI backend.
//
// The frontend calls relative URLs like `/api/v1/reviews/media/{id}` and
// `/api/v1/ratings` via $fetch, which hit the Nuxt (Nitro) server. Without a
// matching server route Nitro returns "Page not found". This handler forwards
// any /api/v1 request that isn't covered by a more specific route file to the
// backend, preserving the method, query string, JSON body and auth token.
export default defineEventHandler(async (event) => {
  const path = getRouterParam(event, 'path') || '';
  const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
  const method = event.method;
  const query = getQuery(event);

  const headers: Record<string, string> = {};
  const token = getCookie(event, 'auth_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  let body: unknown = undefined;
  if (method !== 'GET' && method !== 'HEAD') {
    body = await readBody(event);
  }

  try {
    return await $fetch(`${backendUrl}/api/v1/${path}`, {
      method,
      query,
      headers,
      body,
    });
  } catch (error: any) {
    throw createError({
      statusCode: error.statusCode || error.response?.status || 500,
      statusMessage:
        error.data?.error || error.data?.detail || 'Backend request failed',
      data: error.data,
    });
  }
});
