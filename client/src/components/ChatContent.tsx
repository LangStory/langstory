import { ArrowRightIcon, PaperClipIcon } from '@heroicons/react/24/outline'
import Chat from 'types/Chat.ts'
import Message from 'types/Message.ts'
import { FormEvent, useEffect, useState } from 'react'
import axios from 'axios'
import { URLS } from 'lib/constants.ts'
import { useNavigate } from 'react-router-dom'
import { classNames } from 'lib/helpers.ts'

interface Properties {
    chat: Chat | undefined | null
}

export default function ChatContent({chat}: Properties) {
    const navigate = useNavigate()
    const [message, setMessage] = useState<string | null>(null)
    const [displayMessages, setDisplayMessages] = useState<Message[]>([])
    const [timestamp, setTimestamp] = useState<string | null>(null)

    useEffect(() => {
        if (chat) {
            axios.get(URLS.GET_CHAT_MESSAGES(chat.id))
                .then(({data}) => {
                    setDisplayMessages(data.items)
                })
        }
    }, [chat])

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault()
        const timestamp = new Date().toISOString()
        await axios.post(URLS.CREATE_NEW_MESSAGE(chat!.id), {type: 'user_message', content: message, timestamp})
        navigate(0)
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
                <div className="w-full h-full p-10 flex flex-col flex-grow space-y-10">
                    {displayMessages.map((message: Message) => {
                        return (
                            <div key={message.id} className={classNames('p-6 rounded', message.type === 'system_message' ? 'bg-amber-400' : 'bg-sky-400 ')}>{message.content}</div>
                        )
                    })}
                </div>

                {/*=================================*/}
                {/*MESSAGE INPUT*/}
                {/*=================================*/}
                <div className="w-full px-10 py-3 border-t border-t-gray-300">
                    <form className="w-full p-3 bg-gray-200 flex items-center space-x-4 border-b border-b-black" onSubmit={handleSubmit}>

                        <div className="flex flex-grow space-x-4">
                            <PaperClipIcon className="w-6 h-6"/>
                            <input type="text" className="w-full bg-gray-200 border-none text-black" placeholder="Message ChatBot" onChange={(e) => setMessage(e.target.value)}/>
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