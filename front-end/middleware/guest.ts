export default defineNuxtRouteMiddleware(async () => {
  const { isAuthenticated, restoreSession } = useAuth()

  if (!isAuthenticated.value) {
    await restoreSession()
  }

  if (isAuthenticated.value) {
    const { user } = useAuth()
    return navigateTo(user.value?.id ? `/users/${user.value.id}` : '/users/profile')
  }
})
