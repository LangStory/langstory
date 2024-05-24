import defaultTheme from 'tailwindcss/defaultTheme.js'

/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './index.html',
        './src/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {
            fontFamily: {
                ibm: [ '\'IBM Plex Sans\'', ...defaultTheme.fontFamily.sans ],
            }
        },
    },
    plugins: [],
}