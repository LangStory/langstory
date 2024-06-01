import { ErrorBoundary, Provider } from '@rollbar/react'
import { BrowserRouter } from 'react-router-dom'
import Rollbar from 'rollbar'
import { Toaster } from 'react-hot-toast'
import init from 'lib/init.ts'
import { AuthProvider, useAuth } from 'hooks/use-auth.tsx'
import ErrorFallbackUI from 'components/core/ErrorFallbackUI.tsx'
import Routes from 'components/routing/Routes.tsx'

export default function App() {
    const {updateAuth} = useAuth()
    const {rollbar} = init(updateAuth)

    return (
        <Provider instance={rollbar}>
            <ErrorBoundary fallbackUI={ErrorFallbackUI}>
                <AuthProvider>
                    <BrowserRouter>
                        <Toaster position="bottom-right" reverseOrder={false}/>
                        <Routes/>
                    </BrowserRouter>
                </AuthProvider>
            </ErrorBoundary>
        </Provider>
    )
}
