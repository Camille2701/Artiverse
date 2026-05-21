import type { Auth } from '~/types/auth'
import type { User } from '~/types/user'

export default defineEventHandler(async (event) => {
  const body = await readBody<Auth>(event)

  if (!body?.username && !body?.email || !body?.password) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Username or email, and password are required'
    })
  }

  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const response = await $fetch<{user: User; token: string}>(`${backendUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        username: body.username,
        email: body.email,
        password: body.password
      }
    });

    // Set auth token as cookie
    setCookie(event, 'auth_token', response.token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7 // 1 week
    })

    return response;
  } catch (error: any) {
    console.error('Login error:', error);

    throw createError({
      statusCode: error.statusCode || 401,
      statusMessage: error.data?.detail || 'Login failed'
    });
  }
})