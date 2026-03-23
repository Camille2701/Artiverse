import type { Auth } from '../../types/auth'
import type { User } from '../../types/user'

const DEMO_PASSWORD = 'password123'

export default defineEventHandler(async (event) => {
  const body = await readBody<Auth>(event)

  if (!body?.email || !body?.password) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Email et mot de passe requis'
    })
  }

  const users = await $fetch<User[]>('/api/users', {
    baseURL: getRequestURL(event).origin
  })

  const user = users.find((candidate) => candidate.email.toLowerCase() === body.email.toLowerCase())

  if (!user || body.password !== DEMO_PASSWORD) {
    throw createError({
      statusCode: 401,
      statusMessage: 'Identifiants invalides'
    })
  }

  return {
    user,
    token: `mock-token-${user.id}-${Date.now()}`
  }
})