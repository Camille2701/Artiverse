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
            fontFamily: {
                'display': ['"Space Grotesk"', 'sans-serif'],
                'heading': ['"Outfit"', 'sans-serif'],
                'body': ['"Inter"', 'sans-serif'],
            },
            colors: {
                // Graphical Charter Colors
                // Background colors for dark mode
                'bg-primary': '#12121A',
                'bg-secondary': '#1E1E28',
                'bg-tertiary': '#2A2A38',

                // Text colors
                'text-primary': '#FFFFFF',
                'text-secondary': '#A0A0B0',
                'text-tertiary': '#707080',

                // Border colors
                'border-color': '#2A2A38',
                'border-color-light': '#3A3A48',

                // Media type accent colors
                'accent-movie': '#FF4757',
                'accent-movie-hover': '#E03E4D',
                'accent-series': '#9B51E0',
                'accent-series-hover': '#8A44D0',
                'accent-game': '#00D2D3',
                'accent-game-hover': '#00B9BA',
                'accent-book': '#ECCC68',
                'accent-book-hover': '#D4B85F',

                // Original accent colors (for compatibility)
                accent: '#6366f1',
                'accent-hover': '#4f46e5',
                'accent-light': '#e0e7ff',
            },
            boxShadow: {
                'glow': '0 0 20px rgba(99, 102, 241, 0.4)',
                'glow-movie': '0 0 20px rgba(255, 71, 87, 0.4)',
                'glow-series': '0 0 20px rgba(155, 81, 224, 0.4)',
                'glow-game': '0 0 20px rgba(0, 210, 211, 0.4)',
                'glow-book': '0 0 20px rgba(236, 204, 104, 0.4)',
                'glass': '0 8px 32px rgba(0, 0, 0, 0.4)',
            },
            backdropBlur: {
                'glass': '12px',
            },
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'float': 'float 3s ease-in-out infinite',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0px)' },
                    '50%': { transform: 'translateY(-10px)' },
                }
            }
        }
    }
} satisfies Config