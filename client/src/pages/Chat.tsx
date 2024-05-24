import { PlusIcon, PaperClipIcon, ArrowRightIcon } from '@heroicons/react/24/outline'

export default function Chat() {

    return (
        <div className="w-full h-screen flex font-ibm">
            <div className="w-1/5 h-full pt-10 px-8 flex flex-col items-center space-y-20 bg-gray-100">

                <div className="flex items-center">
                    <PlusIcon className="w-5 h-5"/>
                    <span className="ml-2 font-medium">New Chat</span>
                </div>

                <div className="w-full flex flex-col">
                    <div className="w-full font-medium pb-1 border-b border-b-black">Unread</div>
                </div>

                <div className="w-full flex flex-col">
                    <div className="w-full font-medium pb-1 border-b border-b-black">Summarize</div>
                </div>

                <div className="w-full flex flex-col">
                    <div className="w-full font-medium pb-1 border-b border-b-black">Chats</div>
                </div>

            </div>

            <div className="w-full h-full flex flex-col">
                <div className="w-full flex flex-col justify-center h-14 px-10 border-b border-b-gray-300">
                    <h1 className="font-bold">DATE</h1>
                </div>

                <div className="w-full h-full p-10 flex flex-grow">
                    CHAT CONTENT
                </div>

                <div className="w-full px-10 py-3 border-t border-t-gray-300">

                    <form className="w-full p-3 bg-gray-200 flex items-center space-x-4 border-b border-b-black" onSubmit={e => e.preventDefault()}>

                        <div className="flex flex-grow space-x-4">
                            <PaperClipIcon className="w-6 h-6"/>
                            <input type="text" className="w-full bg-gray-200 border-none text-black" placeholder="Message ChatBot"/>
                        </div>

                        <div className="self-end rounded-full bg-black text-gray-200">
                            <ArrowRightIcon className="w-6 h-6"/>
                        </div>
                    </form>

                </div>
            </div>
        </div>
    )
}
