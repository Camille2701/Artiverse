import type { Auth } from '~/types/auth'
import type { User } from '~/types/user'

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

    // Set auth token as cookie
    setCookie(event, 'auth_token', response.token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7 // 1 week
    })

    return response;
  } catch (error: any) {
    console.error('Registration error:', error);
    console.error('Error details:', JSON.stringify(error, null, 2));

    // Extract error details from different possible error structures
    let errorMessage = 'Registration failed';
    let statusCode = 500;

    if (error?.response) {
      // Nuxt $fetch error structure
      statusCode = error.response.status || 500;
      errorMessage = error.response._data?.detail ||
                    error.response._data?.message ||
                    error.response._data?.error ||
                    'Registration failed';
    } else if (error?.data) {
      // Direct error structure
      statusCode = error.statusCode || 500;
      errorMessage = error.data?.detail ||
                    error.data?.message ||
                    'Registration failed';
    } else if (error?.statusCode) {
      statusCode = error.statusCode;
      errorMessage = error.message || 'Registration failed';
    } else if (typeof error === 'string') {
      errorMessage = error;
    }

    throw createError({
      statusCode,
      statusMessage: errorMessage
    });
  }
})