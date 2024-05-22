import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'
import Rollbar from 'rollbar'
import { StatusCodes } from 'http-status-codes'
import toast from 'react-hot-toast'
import mixpanel from 'mixpanel-browser'
import { deleteValue, getValue, STORAGE_KEYS } from './session-manager.ts'
import { jwtDecode, JwtPayload } from 'jwt-decode'

export default function init(rollbar: Rollbar, updatedAuth: () => void) {

    //--------------------
    // AXIOS
    //--------------------
    axios.interceptors.request.use(
        (config: InternalAxiosRequestConfig) => {
            const jwt: string = getValue(STORAGE_KEYS.ACCESS_TOKEN)

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

    axios.interceptors.response.use(undefined, (error: AxiosError) => {
        if (error.response) {
            if (error.response.status === StatusCodes.UNAUTHORIZED && window.location.pathname !== '/login') {
                deleteValue(STORAGE_KEYS.ACCESS_TOKEN)
                updatedAuth()
                window.location.replace('/login')
            }
        } else if ((error.toJSON() as Error).message === 'Network Error' && !window.navigator.onLine) {
            toast('You have no internet connection', {icon: '⚠️', duration: 5000})
        } else {
            rollbar.error(error)
        }

        return Promise.reject(error)
    })


    //--------------------
    // MIXPANEL
    //--------------------
    if (process.env.NODE_ENV === 'production') mixpanel.init('9e21912804890c28dc6cbbf8632850bc', {track_pageview: true, persistence: 'localStorage'})
    else mixpanel.init('notavalidtoken', {track_pageview: true, persistence: 'localStorage'})
}
