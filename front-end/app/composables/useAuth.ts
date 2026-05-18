import type { Auth } from '~/types/auth'
import type { User } from '~/types/user'

export const useAuth = () => {
  const user = useState<User | null>('authUser', () => null)
  const token = useState<string | null>('authToken', () => null)

  const isAuthenticated = computed(() => !!user.value && !!token.value)

  async function login(auth: Auth) {
    const res = await $fetch<{user: User; token: string}>('/api/login', {
      method: 'POST',
      body: auth
    })

    user.value = res.user
    token.value = res.token
  }

  function logout() {
    user.value = null
    token.value = null
  }

  return { user, token, isAuthenticated, login, logout }
}