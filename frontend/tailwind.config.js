/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                strava: {
                    orange: '#FC4C02',
                    'orange-dark': '#E34402',
                    gray: {
                        50: '#F7F7FA',
                        100: '#EFEFEF',
                        200: '#DFDFE3',
                        300: '#B0B0B8',
                        400: '#8B8B94',
                        500: '#6D6D78',
                        600: '#4F4F5C',
                        700: '#38383F',
                        800: '#242428',
                        900: '#1A1A1E',
                    }
                }
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
