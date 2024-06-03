import { ArrowRightIcon, PaperClipIcon } from '@heroicons/react/24/outline'
import Chat from 'types/Chat.ts'
import Message from 'types/Message.ts'
import { FormEvent, useEffect, useRef, useState } from 'react'
import axios from 'axios'
import Nullable from 'types/Nullable.ts'
import Optional from 'types/Optional.ts'
import { URLS } from 'lib/constants.ts'
import MessageComponent from 'components/MessageComponent.tsx'

interface Properties {
    chat: Nullable<Optional<Chat>>
}

export default function ChatContent({chat}: Properties) {
    const messageScroll = useRef<HTMLDivElement>(null)
    const [message, setMessage] = useState<Nullable<string>>(null)
    const [displayMessages, setDisplayMessages] = useState<Array<Message>>([])
    const [timestamp, setTimestamp] = useState<string>(new Date().toISOString())

    useEffect(() => {
        if (chat) {
            axios.get(URLS.GET_CHAT_MESSAGES(chat.id))
                .then(({data}) => {
                    setDisplayMessages(data.items)
                })
        }
    }, [chat])

    useEffect(() => {
        if (messageScroll.current) {
            messageScroll.current.scrollIntoView({behavior: 'smooth'})
        }
    }, [displayMessages])

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault()
        const {data} = await axios.post(URLS.CREATE_NEW_MESSAGE(chat!.id), {type: 'user_message', content: message, timestamp})
        setDisplayMessages([...displayMessages, data])
        setMessage(null)
    }

    if (chat) return (
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
                <div className="w-full h-full px-10 pt-10 flex flex-col flex-grow overflow-y-auto">
                    <div className="h-full flex flex-col flex-grow space-y-8 overflow-y-auto">
                        {displayMessages.map((message: Message) =>
                            <MessageComponent message={message}/>
                        )}
                        <div className="h-1" ref={messageScroll}/>
                    </div>
                </div>

                {/*=================================*/}
                {/*MESSAGE INPUT*/}
                {/*=================================*/}
                <div className="w-full flex px-10 py-3 border-t border-t-gray-300">
                    <form className="w-full p-3 bg-gray-200 flex items-center space-x-4 border-b border-b-black" onSubmit={handleSubmit}>

                        <div className="flex flex-grow space-x-4">
                            <PaperClipIcon className="w-6 h-6"/>
                            <input type="text" className="w-full bg-gray-200 border-none text-black" placeholder="Message ChatBot" value={message || ''} onChange={(e) => setMessage(e.target.value)}/>
                        </div>

                        <div className="self-end rounded-full bg-black text-gray-200">
                            <ArrowRightIcon className="w-6 h-6"/>
                        </div>
                    </form>
                </div>
            </div>

        </>
    )

    else return (
        <></>
    )
}