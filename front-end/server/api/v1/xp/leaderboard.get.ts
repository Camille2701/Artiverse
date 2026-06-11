export default defineEventHandler(async (event) => {
  const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
  const query = getQuery(event)
  const headers: Record<string, string> = {}
  const token = getCookie(event, 'auth_token')
  if (token) headers['Authorization'] = `Bearer ${token}`
  return await $fetch(`${backendUrl}/api/v1/xp/leaderboard`, { query, headers })
})
