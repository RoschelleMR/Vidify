/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    fontSize: {
      'heading-xl': '3rem',  // Custom size for large headings (h1)
      'heading-lg': '2rem',    // Custom size for medium headings (h2)
      'heading-md': '1.5rem',  // Custom size for small headings (h3)
      'body-xl': '1.25rem',    // Extra large body text
      'body-lg': '1.125rem',   // Larger body text
      'body-base': '1rem',     // Standard body text
      'body-sm': '0.875rem',   // Small body text
      'body-tiny': '0.75rem',  // Tiny body text
      },
    extend: {
      fontFamily: {
        heading: ['Montserrat', 'sans-serif'],
        body: ['Montserrat', 'sans-serif'],
        nav: ['Palanquin', 'sans-serif'],
        button: ['Palanquin', 'sans-serif'],
      },
      colors: {
        'primary': "#1bf84e",
        'secondary': "#F3F4F6",
        'accent': "#b9febe",
        body: {
          default: "#000",
          slate: "#848484",
          alt: "#fff",
        },
      },
    },
  },
  plugins: [],
}

