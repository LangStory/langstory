import React, { useState, useEffect, ReactNode, useContext } from 'react'
import axios, { AxiosError, AxiosResponse } from 'axios'
import { useNavigate } from 'react-router-dom'
import { jwtDecode } from 'jwt-decode'
import { StatusCodes } from 'http-status-codes'
import { useRollbarPerson } from '@rollbar/react'
import mixpanel from 'mixpanel-browser'
import Nullable from '@typing/Nullable.ts'
import RefreshTokenResponse from '@typing/Auth.ts'
import { AuthJwtPayload } from '@typing/AuthJwtPayload.ts'
import { deleteValue, getValue, STORAGE_KEYS, storeValue } from '@lib/session-manager'
import { URLS } from '@lib/constants'

function tokenExpired(token: string | null): boolean {
    if (token) {
        const decoded: AuthJwtPayload = jwtDecode<AuthJwtPayload>(token)
        return !jwtIsValid(decoded)
    } else return true
}

function jwtIsValid(decoded: AuthJwtPayload): boolean {
    try {
        return !!decoded && !!decoded.exp && decoded.exp > (Date.now() / 1000)
    } catch (error) {
        console.error('Error decoding token:', error)
        return false
    }
}

interface AuthContext {
    user: Nullable<AuthJwtPayload>;
    validateJwtToken: () => Promise<void>;
    refreshAccessToken: () => Promise<void>;
    accessTokenExpired: () => boolean;
    refreshTokenExpired: () => boolean;
    signOut: () => void;
}

const Context: React.Context<AuthContext> = React.createContext<AuthContext>({
    user: null,
    validateJwtToken: async () => {
    },
    refreshAccessToken: async () => {
    },
    accessTokenExpired: () => true,
    refreshTokenExpired: () => true,
    signOut: () => {
    },
})

export function AuthProvider({children}: { children: ReactNode }) {
    const navigate = useNavigate()
    const [user, setUser] = useState<Nullable<AuthJwtPayload>>(null)
    const [loading, setLoading] = useState<boolean>(true)
    const [error, setError] = useState<string>('')
    useRollbarPerson(user as object)

    async function getNewAuthToken(token: string) {
        try {
            const response: AxiosResponse<RefreshTokenResponse> = await axios.post<RefreshTokenResponse>(URLS.REFRESH_TOKEN(), {token})
            if (response.status === StatusCodes.OK) {
                const data: RefreshTokenResponse = response.data
                if (data.data) {
                    const token: string = data.token
                    const email: string = data.data.user.email_address || 'UNDEFINED_USER'
                    const name: string = `${data.data.user.first_name} ${data.data.user.last_name}` || 'UNDEFINED_NAME'
                    storeValue(STORAGE_KEYS.ACCESS_TOKEN, token)
                    mixpanel.identify(email)
                    mixpanel.people.set_once({$email: email, $name: name})
                    mixpanel.people.set({email})
                    await validateJwtToken()
                }
            } else setError('Couldn\'t log in.')
        } catch (e) {
            const error: AxiosError = e as AxiosError
            if (error.request && error.request.status === StatusCodes.UNAUTHORIZED) {
                setError('Failed to refresh token')
            } else {
                setError((e as Error).message)
            }
        }
    }

    async function refreshAccessToken() {
        const token: Nullable<string> = getValue(STORAGE_KEYS.REFRESH_TOKEN)
        if (token) {
            try {
                const decoded: AuthJwtPayload = jwtDecode<AuthJwtPayload>(token)
                if (jwtIsValid(decoded)) {
                    // Refresh token is still valid, reset access token
                    await getNewAuthToken(token)
                } else {
                    // Refresh token is expired or invalid
                    setUser(null)
                }
            } catch (error) {
                console.error('Error decoding refresh token:', error)
                setUser(null)
            }
        } else {
            setUser(null)
        }
    }

    async function validateJwtToken() {
        const token: Nullable<string> = getValue(STORAGE_KEYS.ACCESS_TOKEN)
        if (token) {
            try {
                const decoded: AuthJwtPayload = jwtDecode<AuthJwtPayload>(token)
                if (jwtIsValid(decoded)) {
                    setUser(decoded)
                } else {
                    // Token is expired or invalid
                    await refreshAccessToken()
                }
            } catch (error) {
                console.error('Error auth decoding token:', error)
                setUser(null)
            }
        } else {
            await refreshAccessToken()
        }
    }

    function clearTokens() {
        deleteValue(STORAGE_KEYS.ACCESS_TOKEN)
        deleteValue(STORAGE_KEYS.REFRESH_TOKEN)
    }

    function signOut() {
        clearTokens()
        setUser(null)
        navigate('/login')
    }

    function accessTokenExpired() {
        const token: Nullable<string> = getValue(STORAGE_KEYS.ACCESS_TOKEN)
        return tokenExpired(token)
    }

    function refreshTokenExpired() {
        const token: Nullable<string> = getValue(STORAGE_KEYS.REFRESH_TOKEN)
        return tokenExpired(token)
    }

    useEffect(() => {
        validateJwtToken().then(() => setLoading(false))
    }, [])

    return (
        <Context.Provider value={{
            user,
            validateJwtToken,
            refreshAccessToken,
            accessTokenExpired,
            refreshTokenExpired,
            signOut
        }}>
            {!loading && children}
        </Context.Provider>
    )
}

export function useAuth() {
    return useContext<AuthContext>(Context)
}
