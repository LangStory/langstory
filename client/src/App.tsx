import { ErrorBoundary, Provider } from '@rollbar/react'
import { BrowserRouter } from 'react-router-dom'
import Rollbar from 'rollbar'
import { Toaster } from 'react-hot-toast'
import init from 'lib/init.ts'
import { AuthProvider, useAuth } from 'hooks/use-auth.tsx'
import ErrorFallbackUI from 'components/core/ErrorFallbackUI.tsx'
import Routes from 'components/routing/Routes.tsx'

const rollbar = new Rollbar({
    accessToken: 'notavalidtoken',
    captureUncaught: true,
    captureUnhandledRejections: true,
    enabled: process.env.NODE_ENV === 'production',
    payload: {
        environment: process.env.NODE_ENV,
        server: {root: 'https://app.langstory.org'}
    }
})

export default function App() {
    const {updateAuth} = useAuth()
    init(rollbar, updateAuth)

    return (
        <Provider instance={rollbar}>
            <ErrorBoundary fallbackUI={ErrorFallbackUI}>
                <AuthProvider>
                    <BrowserRouter>
                        <Toaster position="top-center" reverseOrder={false}/>
                        <Routes/>
                    </BrowserRouter>
                </AuthProvider>
            </ErrorBoundary>
        </Provider>
    )
}
