import { ReactNode } from 'react'

interface Properties {
    children: ReactNode;
}

export default function Navbar({children}: Properties) {
    return (
        <div className="w-full h-full flex">
            <div className="w-full h-full flex-grow">
                {children}
            </div>
        </div>
    )
}
