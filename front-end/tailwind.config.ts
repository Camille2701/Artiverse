import type { Config } from 'tailwindcss'

export default {
    darkMode: 'class',
    content: [
        "./pages/**/*.{js,vue,ts}",
        "./components/**/*.{js,vue,ts}",
        "./layouts/**/*.vue",
        "./app.vue",
        "./plugins/**/*.{js,ts}",
        "./composables/**/*.{js,ts}"
    ],
    theme: {
        extend: {
            colors: {
                // Graphical Charter Colors
                // Background colors for dark mode
                'bg-primary': '#12121A',
                'bg-secondary': '#1E1E28',
                'bg-tertiary': '#2A2A38',

                // Media type accent colors
                'accent-movie': '#FF4757',
                'accent-series': '#9B51E0',
                'accent-game': '#00D2D3',
                'accent-book': '#ECCC68',

                // Original accent colors (for compatibility)
                accent: '#6366f1',
                'accent-hover': '#4f46e5',
                'accent-light': '#e0e7ff',
            }
        }
    }
} satisfies Config