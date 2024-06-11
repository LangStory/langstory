import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'
import Rollbar from 'rollbar'
import { StatusCodes } from 'http-status-codes'
import mixpanel from 'mixpanel-browser'
import { getValue, STORAGE_KEYS } from './session-manager.ts'
import Nullable from '../typing/Nullable.ts'

export default function init(validateJwtToken: () => Promise<void>): { rollbar: Rollbar } {
    //==============================
    // ROLLBAR
    //==============================
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

    //==============================
    // AXIOS
    //==============================
    axios.interceptors.request.use(
        (config: InternalAxiosRequestConfig) => {
            const jwt: Nullable<string> = getValue(STORAGE_KEYS.ACCESS_TOKEN)

            if (jwt) {
                config.headers['Authorization'] = `Bearer ${jwt}`
                return config
            }

            return config
        },
        (error: Error) => {
            console.log(error)
            window.location.replace('/login')
        }
    )

    axios.interceptors.response.use(undefined, async (error: AxiosError) => {
        if (error.response) {
            if (error.response.status === StatusCodes.UNAUTHORIZED && window.location.pathname !== '/login') {
                try {
                    await validateJwtToken()
                    setTimeout(() => window.location.reload(), 1)
                    const jwt: Nullable<string> = getValue(STORAGE_KEYS.ACCESS_TOKEN)
                    if (jwt && error && error.config) {
                        error.config.headers['Authorization'] = `Bearer ${jwt}`
                        return axios(error.config)
                    }
                } catch (tokenError) {
                    window.location.replace('/login')
                }
            } else if (error.response.status === StatusCodes.FORBIDDEN) {
                window.location.replace('/login')
            }
        } else {
            rollbar.error(error)
        }

        return Promise.reject(error)
    })

    //==============================
    // MIXPANEL
    //==============================
    if (process.env.NODE_ENV === 'production') mixpanel.init('notavalidtoken', {track_pageview: true, persistence: 'localStorage'})
    else mixpanel.init('notavalidtoken', {track_pageview: true, persistence: 'localStorage'})

    //==============================
    // RETURN ROLLBAR INSTANCE
    //==============================
    return {rollbar}
}
