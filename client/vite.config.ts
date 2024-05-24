import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            'pages': path.resolve(__dirname, './src/pages'),
            'components': path.resolve(__dirname, './src/components'),
            'hooks': path.resolve(__dirname, './src/hooks'),
            'lib': path.resolve(__dirname, './src/lib'),
            'types': path.resolve(__dirname, './src/types'),
            'assets': path.resolve(__dirname, './src/assets'),
            'services': path.resolve(__dirname, './src/services'),
        }
    }
})
