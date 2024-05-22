import { ReactNode } from 'react'
import { ClipboardDocumentListIcon, ClipboardDocumentCheckIcon, QrCodeIcon, AdjustmentsVerticalIcon } from '@heroicons/react/24/outline'
import { Link } from 'react-router-dom'

interface Properties {
    children: ReactNode;
}

export default function Navbar({children}: Properties) {
    return (
        <div className="w-full h-full flex flex-col">
            <div className="flex-grow">
                {children}
            </div>
            <div className="w-full h-14 bg-blue-500 text-white">
                <div className="w-full h-full px-12 py-2 flex justify-between items-center">
                    <Link to="/receiving-tasks">
                        <ClipboardDocumentListIcon className="w-6 h-6"/>
                    </Link>

                    <Link to="/qr-reader">
                        <QrCodeIcon className="w-6 h-6"/>
                    </Link>

                    <Link to="/picking-job">
                        <ClipboardDocumentCheckIcon className="w-6 h-6"/>
                    </Link>

                    <Link to="/settings">
                        <AdjustmentsVerticalIcon className="w-6 h-6"/>
                    </Link>
                </div>
            </div>
        </div>
    )
}
