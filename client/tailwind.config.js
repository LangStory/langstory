import defaultTheme from 'tailwindcss/defaultTheme.js'

/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './index.html',
        './src/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {
            fontSize: {
                '2xs': '0.625rem'
            },
            fontFamily: {
                ibm: [ '\'IBM Plex Sans\'', ...defaultTheme.fontFamily.sans ],
            }
        },
    },
    plugins: [],
}