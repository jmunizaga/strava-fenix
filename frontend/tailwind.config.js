/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                fenix: {
                    orange: '#F37021',
                    'orange-dark': '#D65A10',
                    black: '#000000',
                    gray: {
                        50: '#F9F9F9',
                        100: '#F5F5F5',
                        200: '#E5E5E5',
                        300: '#D4D4D4',
                        400: '#A3A3A3',
                        500: '#737373',
                        600: '#525252',
                        700: '#404040',
                        800: '#262626',
                        900: '#171717',
                    }
                },
                strava: {
                    orange: '#FC4C02',
                }
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
