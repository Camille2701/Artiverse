export const useTheme = () => {
  // Initialize theme from localStorage or system preference
  const theme = useState<'light' | 'dark'>('theme', () => {
    if (process.client) {
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme === 'light' || savedTheme === 'dark') {
        return savedTheme
      }
      // Use system preference as fallback
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
    return 'light'
  })

  const isDark = computed(() => theme.value === 'dark')

  // Apply theme to document
  function applyTheme() {
    if (process.client) {
      const html = document.documentElement
      if (theme.value === 'dark') {
        html.classList.add('dark')
      } else {
        html.classList.remove('dark')
      }
    }
  }

  // Toggle theme
  function toggleTheme() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    if (process.client) {
      localStorage.setItem('theme', theme.value)
    }
    applyTheme()
  }

  // Set specific theme
  function setTheme(newTheme: 'light' | 'dark') {
    theme.value = newTheme
    if (process.client) {
      localStorage.setItem('theme', newTheme)
    }
    applyTheme()
  }

  // Initialize on mount
  onMounted(() => {
    applyTheme()

    // Listen for system preference changes
    if (process.client) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      const handleChange = (e: MediaQueryListEvent) => {
        // Only change if user hasn't manually set a preference
        if (!localStorage.getItem('theme')) {
          theme.value = e.matches ? 'dark' : 'light'
          applyTheme()
        }
      }

      mediaQuery.addEventListener('change', handleChange)

      // Cleanup on unmount
      onUnmounted(() => {
        mediaQuery.removeEventListener('change', handleChange)
      })
    }
  })

  return { theme, isDark, toggleTheme, setTheme }
}