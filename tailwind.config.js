/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'beetle-forest': '#065f46',
        'ice-cyan': '#06b6d4',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        shake: {
          '0%': { transform: 'translate(0,0)' },
          '25%': { transform: 'translate(-5px,0)' },
          '75%': { transform: 'translate(5px,0)' },
          '100%': { transform: 'translate(0,0)' },
        },
        pop: {
          '0%': { transform: 'scale(0.8)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
      animation: {
        'float': 'float 3s ease-in-out infinite',
        'shake': 'shake 0.3s',
        'pop': 'pop 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
      },
      backgroundImage: {
        'forest': 'linear-gradient(to bottom, #065f46, #064e3b)',
        'ice': 'linear-gradient(to bottom, #0369a1, #0c4a6e)',
        'desert': 'linear-gradient(to bottom, #9a3412, #7c2d12)',
        'volcano': 'linear-gradient(to bottom, #991b1b, #7f1d1d)',
        'beetle-forest': 'linear-gradient(to bottom, #065f46, #064e3b)',
      },
    },
  },
  plugins: [],
}
