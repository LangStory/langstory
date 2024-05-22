import React, { useState, useEffect, ReactNode, useContext } from 'react'
import { jwtDecode, JwtPayload } from 'jwt-decode'
import { getValue, STORAGE_KEYS } from '../lib/session-manager'
import { useRollbarPerson } from '@rollbar/react'

interface AuthContext {
    user: JwtPayload | null;
    updateAuth: () => void
}

const Context: React.Context<AuthContext> = React.createContext<AuthContext>({user: null, updateAuth: () => void (0)})

export function AuthProvider({children}: { children: ReactNode }) {
    const [user, setUser] = useState<JwtPayload | null>(null)
    const [loading, setLoading] = useState<boolean>(true)
    useRollbarPerson(user as object)

    function checkToken() {
        const token: string = getValue(STORAGE_KEYS.ACCESS_TOKEN)
        if (token) {
            try {
                const decoded: JwtPayload = jwtDecode<JwtPayload>(token)
                if (decoded && decoded.exp && decoded.exp > Date.now() / 1000) {
                    setUser(decoded)
                } else {
                    // Token is expired or invalid
                    setUser(null)
                }
            } catch (error) {
                console.error('Error decoding token:', error)
                setUser(null)
            }
        } else {
            setUser(null)
        }
    }

    useEffect(() => {
        checkToken()
        setLoading(false)
    }, [])

    return <Context.Provider value={{user, updateAuth: checkToken}}>{!loading && children}</Context.Provider>
}

export function useAuth() {
    return useContext<AuthContext>(Context)
}
