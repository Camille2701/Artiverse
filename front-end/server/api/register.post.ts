import type { Auth } from '../../types/auth'
import type { User } from '../../types/user'

export default defineEventHandler(async (event) => {
  const body = await readBody<Auth>(event)

  if (!body?.username || !body?.email || !body?.password) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Username, email, and password are required'
    })
  }

  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const response = await $fetch<{user: User; token: string}>(`${backendUrl}/api/v1/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        username: body.username,
        email: body.email,
        password: body.password,
        bio: body.bio || '',
        avatar_url: body.avatar_url || ''
      }
    });

    return response;
  } catch (error: any) {
    console.error('Registration error:', error);

    throw createError({
      statusCode: error.statusCode || 400,
      statusMessage: error.data?.detail || 'Registration failed'
    });
  }
})