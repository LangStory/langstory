import { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../hooks/use-auth'

export default function AuthRoute({children}: { children: ReactNode }) {
    const location = useLocation()
    const {user} = useAuth()

    if (user) return <>{children}</>
    return <Navigate to="/login" state={{from: location}} replace/>
}
