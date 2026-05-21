import type { Auth } from '../../types/auth'
import type { User } from '../../types/user'

export default defineEventHandler(async (event) => {
  const body = await readBody<Auth>(event)

  if (!body?.email && !body?.password) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Email ou nom d\'utilisateur et mot de passe requis'
    })
  }

  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const response = await $fetch(`${backendUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        email: body.email,
        password: body.password
      }
    });

    return response;
  } catch (error: any) {
    console.error('Login error:', error);

    // Fallback to mock logic if backend is not available
    const DEMO_PASSWORD = 'password123';

    const users = await $fetch<User[]>('/api/users', {
      baseURL: getRequestURL(event).origin
    });

    const user = users.find((candidate) =>
      candidate.email.toLowerCase() === body.email.toLowerCase() ||
      candidate.username.toLowerCase() === body.email.toLowerCase()
    );

    if (!user || body.password !== DEMO_PASSWORD) {
      throw createError({
        statusCode: 401,
        statusMessage: 'Identifiants invalides'
      })
    }

    return {
      user,
      token: `mock-token-${user.id}-${Date.now()}`
    };
  }
})