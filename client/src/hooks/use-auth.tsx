import React, { useState, useEffect, ReactNode, useContext } from 'react'
import { jwtDecode } from 'jwt-decode'
import { AuthJwtPayload, RefreshJwtPayload } from '../lib/langstory-jwt-decode'
import { getValue, STORAGE_KEYS, storeValue } from '../lib/session-manager'
import { useRollbarPerson } from '@rollbar/react'
import RefreshTokenResponse  from '../types/Auth.ts'
import { StatusCodes } from 'http-status-codes'
import { URLS } from '../lib/constants'
import mixpanel from 'mixpanel-browser'

import axios, { AxiosError, AxiosResponse } from 'axios'

interface AuthContext {
    user: AuthJwtPayload | null;
    updateAuth: () => void
}

const Context: React.Context<AuthContext> = React.createContext<AuthContext>({user: null, updateAuth: () => void (0)})


export function AuthProvider({children}: { children: ReactNode }) {
    const [user, setUser] = useState<AuthJwtPayload | null>(null)
    const [loading, setLoading] = useState<boolean>(true)
    const [error, setError] = useState<string>('')
    useRollbarPerson(user as object)


    async function getNewAuthToken(token: string){
        try {
            const formData = new FormData()
            formData.append('token', token)
            const response: AxiosResponse<RefreshTokenResponse> = await axios.post<RefreshTokenResponse>(URLS.REFRESH_TOKEN(), formData)
            if (response.status === StatusCodes.OK) {
                storeValue(STORAGE_KEYS.ACCESS_TOKEN, response.data.token)
                const token: string = response.data.token
                const email: string = response.data.data.user.email_address || 'UNDEFINED_USER'
                const name: string = `${response.data.data.user.first_name} ${response.data.data.user.last_name}`  || 'UNDEFINED_NAME'
                storeValue(STORAGE_KEYS.ACCESS_TOKEN, token)
                mixpanel.identify(email)
                mixpanel.people.set_once({$email: email, $name: name})
                mixpanel.people.set({email})
                checkToken()
            } else setError('Couldn\'t log in.')
        } catch (e) {
            const error = e as AxiosError
            if (error.request && error.request.status === StatusCodes.UNAUTHORIZED) setError('Failed to refresh token')
            else {
                setError((e as Error).message)
            }
        }
    }

    async function refreshToken(){
        const token: string = getValue(STORAGE_KEYS.REFRESH_TOKEN)
        if (token) {
            try {
                const decoded: RefreshJwtPayload = jwtDecode<RefreshJwtPayload>(token)
                if (decoded && decoded.exp && decoded.exp > Date.now() / 1000) {
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

    async function checkToken() {
        const token: string = getValue(STORAGE_KEYS.ACCESS_TOKEN)
        if (token) {
            try {
                const decoded: AuthJwtPayload = jwtDecode<AuthJwtPayload>(token)
                if (decoded && decoded.exp && decoded.exp > Date.now() / 1000) {
                    setUser(decoded)
                } else {
                    // Token is expired or invalid
                    await refreshToken()
                }
            } catch (error) {
                console.error('Error auth decoding token:', error)
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
