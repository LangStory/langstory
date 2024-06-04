import { ReactNode, useCallback, useEffect } from 'react'

interface Properties {
    displayed: boolean
    setDisplayed: (d: boolean) => void
    children: ReactNode
}

export default function Modal({displayed, setDisplayed, children}: Properties) {
    const escFunction = useCallback((event: KeyboardEvent) => {
        if (event.key === 'Escape') setDisplayed(false)
    }, [])

    useEffect(() => {
        document.addEventListener('keydown', escFunction, false)
        return () => document.removeEventListener('keydown', escFunction, false)
    }, [escFunction])

    if (displayed) return (
        <div className="fixed top-0 left-0 w-screen h-screen flex flex-col justify-center items-center bg-gray-700 bg-opacity-70" onClick={() => setDisplayed(false)}>
            <div className="-mt-96" onClick={e => e.stopPropagation()}>
                {children}
            </div>
        </div>
    )
    else return <></>
}
