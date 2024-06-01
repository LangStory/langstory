import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'

export default function OfflineNotification() {
    const [toastId, setToastId] = useState<string | null>(null)

    // ==========================================
    // OFFLINE NOTIFICATION
    // ==========================================
    useEffect(() => {
        const handleOnline = () => {
            if (toastId) toast.dismiss(toastId)
            else toast.dismiss()
        }

        const handleOffline = () => {
            const id = toast('You are currently offline.', {icon: '⚠️', duration: Infinity, position: 'bottom-left'})
            setToastId(id)
        }

        if (!window.navigator.onLine) {
            handleOffline()
        }

        window.addEventListener('online', handleOnline)
        window.addEventListener('offline', handleOffline)

        return () => {
            window.removeEventListener('online', handleOnline)
            window.removeEventListener('offline', handleOffline)
        }
    }, [])

    return ''
}