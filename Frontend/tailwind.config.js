/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'custom-orange': '#FD9F24',
        'light-yellow': '#FFC42A',
        'bgYellow': '#FFFEFA',  
        'light-gray' : '#CDCDCD',
        'dark-gray' : '#535353',
        'light-orange': '#FD9F24'
      },
    },
  },
  plugins: [],
}