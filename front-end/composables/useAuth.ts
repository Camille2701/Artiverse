import type { Auth } from '~/types/auth'
import type { User } from '~/types/user'

export const useAuth = () => {
  const user = useState<User | null>('authUser', () => null)
  const token = useState<string | null>('authToken', () => null)

  const isAuthenticated = computed(() => !!user.value && !!token.value)

  async function login(auth: Auth) {
    try {
      const res = await $fetch<{user: User; token: string}>('/api/login', {
        method: 'POST',
        body: auth
      })

      user.value = res.user
      token.value = res.token

      // Store token in cookie for server-side requests
      const cookie = useCookie('auth_token', {
        maxAge: 60 * 30, // 30 minutes
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax'
      })
      cookie.value = res.token
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  async function register(auth: Auth) {
    try {
      const res = await $fetch<{user: User; token: string}>('/api/register', {
        method: 'POST',
        body: auth
      })

      user.value = res.user
      token.value = res.token

      // Store token in cookie for server-side requests
      const cookie = useCookie('auth_token', {
        maxAge: 60 * 30, // 30 minutes
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax'
      })
      cookie.value = res.token

      return res
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  }

  function logout() {
    user.value = null
    token.value = null

    // Clear auth token cookie
    const cookie = useCookie('auth_token')
    cookie.value = null
  }

  return { user, token, isAuthenticated, login, register, logout }
}