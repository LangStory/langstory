import { MutableRefObject, useCallback, useRef } from 'react'

export default function useDebounce<T extends Array<any>>(callback: (...args: T) => void, delay: number) {
    const timer: MutableRefObject<NodeJS.Timeout | null> = useRef<NodeJS.Timeout | null>(null)

    const debouncedCallback = useCallback((...args: T) => {
        if (timer.current) clearTimeout(timer.current)
        timer.current = setTimeout(() => callback(...args), delay)
    }, [callback, delay])

    return debouncedCallback
}