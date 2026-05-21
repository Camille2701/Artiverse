export interface ApiError {
  statusCode?: number
  statusMessage?: string
  message?: string
  data?: any
}

export const useApi = () => {
  const isLoading = ref(false)
  const error = ref<ApiError | null>(null)

  const fetchWithAuth = async <T>(url: string, options: RequestInit = {}): Promise<T> => {
    const cookie = useCookie('auth_token')
    const token = cookie.value

    isLoading.value = true
    error.value = null

    try {
      const response = await $fetch<T>(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': token ? `Bearer ${token}` : '',
          'Content-Type': 'application/json'
        }
      })
      return response
    } catch (err: any) {
      error.value = {
        statusCode: err.statusCode,
        statusMessage: err.statusMessage,
        message: err.message,
        data: err.data
      }
      throw error.value
    } finally {
      isLoading.value = false
    }
  }

  const getErrorMessage = (error: ApiError | null): string => {
    if (!error) return 'Une erreur est survenue'

    if (error.statusMessage) return error.statusMessage
    if (error.message) return error.message
    if (error.data?.detail) return error.data.detail

    switch (error.statusCode) {
      case 400:
        return 'Données invalides'
      case 401:
        return 'Non autorisé. Veuillez vous connecter.'
      case 403:
        return 'Accès refusé'
      case 404:
        return 'Ressource non trouvée'
      case 500:
        return 'Erreur serveur. Veuillez réessayer plus tard.'
      default:
        return 'Une erreur est survenue'
    }
  }

  return {
    isLoading,
    error,
    fetchWithAuth,
    getErrorMessage,
    clearError: () => { error.value = null }
  }
}