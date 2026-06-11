import type { Auth } from '../../types/auth'

export default defineEventHandler(async (event) => {
  const body = await readBody<Auth>(event)

  // Support both email and username
  const emailOrUsername = body?.email || body?.username
  const password = body?.password

  if (!emailOrUsername || !password) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Email ou nom d\'utilisateur et mot de passe requis'
    })
  }

  const backendUrl = process.env.BACKEND_URL || 'http://backend:8000'

  // Prepare login data - support both email and username
  const loginData: Record<string, string> = {
    password: password
  }

  // Check if it's an email or username
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (emailRegex.test(emailOrUsername)) {
    loginData.email = emailOrUsername
  } else {
    loginData.username = emailOrUsername
  }

  try {
    const response = await $fetch(`${backendUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: loginData
    })

    return response
  } catch (error: any) {
    // Extract error message from FastAPI response
    const detail = error?.data?.detail || error?.message || 'Identifiants invalides'
    const status = error?.statusCode || error?.response?.status || 401

    throw createError({
      statusCode: status,
      statusMessage: detail
    })
  }
})