import { ErrorBoundary, Provider } from '@rollbar/react'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import init from 'lib/init.ts'
import { AuthProvider, useAuth } from 'hooks/use-auth.tsx'
import ErrorFallbackUI from 'components/core/ErrorFallbackUI.tsx'
import OfflineNotification from 'components/core/OfflineNotification.tsx'
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
                        <OfflineNotification/>
                        <Routes/>
                    </BrowserRouter>
                </AuthProvider>
            </ErrorBoundary>
        </Provider>
    )
}
