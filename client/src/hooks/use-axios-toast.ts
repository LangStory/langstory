import { useCallback } from 'react'
import toast from 'react-hot-toast'
import { useRollbar } from '@rollbar/react'
import { AxiosError, AxiosResponse } from 'axios'
import { ErrorDetail } from '../types.ts'

/**
 * A custom hook for handling Axios requests with toast notifications.
 */
export function useAxiosToast() {
    const rollbar = useRollbar()

    return useCallback(<T>(
        fn: () => Promise<AxiosResponse<T>>,
        options: {
            loading: string,
            success: string,
            error: string,
            onSuccess?: (response: AxiosResponse<T>) => void,
            onError?: (response: AxiosError<{ detail: string }>) => void,
        }
    ) => {
        return toast.promise(
            fn(),
            {
                loading: options.loading,
                success: (response: AxiosResponse<T>) => {
                    if (options.onSuccess) options.onSuccess(response)
                    return options.success
                },
                error: (error: AxiosError<ErrorDetail>) => {
                    const message = `❌  ${options.error}`
                    if (error.response) {
                        const status = error.response.status
                        const detail = error.response.data.detail
                        rollbar.error(message, new Error(`${status}: ${detail}`))
                        return `${message}\n\n${detail}`
                    } else {
                        rollbar.error(message, error)
                        return `${message}\n\n${error.message}`
                    }
                }
            },
            {
                success: {duration: 1500},
                error: {
                    icon: '',
                    style: {textAlign: 'center'},
                    duration: 5000
                },
            }
        )
    }, [rollbar])
}
