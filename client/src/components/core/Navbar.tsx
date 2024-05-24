import { ReactNode } from 'react'
import { PlusIcon } from '@heroicons/react/24/outline'

interface Properties {
    children: ReactNode;
}

export default function Navbar({children}: Properties) {
    return (
        <div className="w-full h-full flex font-ibm">
            <div className="w-full h-full flex-grow">
                {children}
            </div>
        </div>
    )
}
