export default defineNuxtPlugin(() => {
  const html = document.documentElement
  const saved = localStorage.getItem('theme')

  if (saved === 'light') {
    html.classList.remove('dark')
  } else {
    html.classList.add('dark')
  }
})
