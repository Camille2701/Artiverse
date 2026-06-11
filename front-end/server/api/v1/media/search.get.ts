export default defineEventHandler(async (event) => {
  const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
  const query = getQuery(event)

  const headers: Record<string, string> = {}
  const token = getCookie(event, 'auth_token')
  if (token) headers['Authorization'] = `Bearer ${token}`

  try {
    return await $fetch(`${backendUrl}/api/v1/media/search`, {
      query,
      headers,
    })
  } catch (error: any) {
    throw createError({
      statusCode: error.statusCode || error.response?.status || 500,
      statusMessage: error.data?.detail || 'Search failed',
      data: error.data,
    })
  }
})
