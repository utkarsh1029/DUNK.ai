/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#5EEAD4',
          DEFAULT: '#14B8A6',
          dark: '#0D9488',
        },
        dark: {
          bg: '#070E10',
          card: '#0B1214',
          border: '#151C1F',
        }
      },
    },
  },
  plugins: [],
}

