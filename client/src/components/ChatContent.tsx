import { ArrowRightIcon, PaperClipIcon } from '@heroicons/react/24/outline'
import Chat from 'types/Chat.ts'
import Message from 'types/Message.ts'

interface Properties {
    chat: Chat | undefined | null
}

export default function ChatContent({chat}: Properties) {
    if (chat)
        return (
            <>
                {/*=================================*/}
                {/*CHAT CONTENT*/}
                {/*=================================*/}
                <div className="w-full h-full flex flex-col">

                    {/*=================================*/}
                    {/*DATE*/}
                    {/*=================================*/}
                    <div className="w-full flex flex-col justify-center h-14 px-10 border-b border-b-gray-300">
                        <h1 className="font-bold">{chat.name}</h1>
                    </div>

                    {/*=================================*/}
                    {/*CHAT*/}
                    {/*=================================*/}
                    <div className="w-full h-full p-10 flex flex-grow space-y-10">
                        {chat.messages.map((message: Message) => {
                            return (
                                <div key={message.id} className="p-6 bg-sky-400 rounded">{message.content}</div>
                            )
                        })}
                    </div>

                    {/*=================================*/}
                    {/*MESSAGE INPUT*/}
                    {/*=================================*/}
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

            </>
        )

    else
        return (
            <></>
        )
}