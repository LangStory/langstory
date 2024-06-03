import { MutableRefObject, useCallback, useRef } from 'react'
import Nullable from 'types/Nullable.ts'

export default function useDebounce<T extends Array<any>>(callback: (...args: T) => void, delay: number) {
    const timer: MutableRefObject<Nullable<NodeJS.Timeout>> = useRef<Nullable<NodeJS.Timeout>>(null)

    const debouncedCallback = useCallback((...args: T) => {
        if (timer.current) clearTimeout(timer.current)
        timer.current = setTimeout(() => callback(...args), delay)
    }, [callback, delay])

    return debouncedCallback
}