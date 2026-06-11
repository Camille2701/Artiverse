import type { User, UserUpdate, PasswordUpdate } from '~/types/user'

export const useUsers = () => {
  const { fetchWithAuth } = useApi()
  const { user: currentUser } = useAuth()

  async function getUserById(id: string): Promise<User> {
    return await $fetch<User>(`/api/v1/users/${id}`)
  }

  async function getCurrentUser(): Promise<User> {
    if (!currentUser.value) {
      throw new Error('User not authenticated')
    }
    return await $fetch<User>(`/api/v1/users/${currentUser.value.id}`)
  }

  async function updateUser(id: string, updates: UserUpdate): Promise<User> {
    return await fetchWithAuth<User>(`/api/v1/users/${id}`, {
      method: 'PUT',
      body: updates
    })
  }

  async function updateCurrentUser(updates: UserUpdate): Promise<User> {
    if (!currentUser.value) {
      throw new Error('User not authenticated')
    }
    return await fetchWithAuth<User>(`/api/v1/users/${currentUser.value.id}`, {
      method: 'PUT',
      body: updates
    })
  }

  async function updatePassword(passwordData: PasswordUpdate): Promise<{ message: string }> {
    if (!currentUser.value) {
      throw new Error('User not authenticated')
    }
    return await fetchWithAuth(`/api/v1/users/${currentUser.value.id}/password`, {
      method: 'PUT',
      body: passwordData
    })
  }

  async function deleteUser(id: string): Promise<void> {
    await fetchWithAuth(`/api/v1/users/${id}`, {
      method: 'DELETE'
    })
  }

  async function searchUsers(query: string, params?: { skip?: number; limit?: number }): Promise<{
    items: User[]
    total: number
  }> {
    const queryString = new URLSearchParams({ query, ...params }).toString()
    return await $fetch(`/api/v1/users/search?${queryString}`)
  }

  return {
    getUserById,
    getCurrentUser,
    updateUser,
    updateCurrentUser,
    updatePassword,
    deleteUser,
    searchUsers
  }
}