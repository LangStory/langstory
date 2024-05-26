import { PlusIcon } from '@heroicons/react/24/outline'
import axios from 'axios'
import Chat from 'types/Chat.ts'
import { URLS } from 'lib/constants.ts'
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import ChatContent from 'components/ChatContent.tsx'

export default function ChatComponent() {
    const navigate = useNavigate()
    const {id: chatId} = useParams()
    const [chat, setChat] = useState<Chat | null>()

    useEffect(() => {
        async function fetchChat() {
            if (chatId) {
                const {data} = await axios.get<Chat>(URLS.GET_CHAT(chatId))
                setChat(data)
            }
        }

        fetchChat().then()
    }, [chatId])

    async function newChat() {
        try {
            const {data} = await axios.post<Chat>(URLS.CREATE_NEW_CHAT(), {
                name: (new Date()).toDateString(),
                project_id: '1'
            })
            navigate(`/chat/${data.id}`)
        } catch (e) {
            console.error(e)
            return
        }
    }

    return (
        <div className="w-full h-screen flex font-ibm">

            {/*=================================*/}
            {/*SIDEBAR*/}
            {/*=================================*/}
            <div className="w-1/5 h-full pt-10 px-8 flex flex-col items-center space-y-20 bg-gray-100">
                {/*=================================*/}
                {/*NEW CHAT BUTTON*/}
                {/*=================================*/}
                <button className="flex items-center" onClick={newChat}>
                    <PlusIcon className="w-5 h-5"/>
                    <span className="ml-2 font-medium">New Chat</span>
                </button>

                {/*=================================*/}
                {/*UNREAD SECTION*/}
                {/*=================================*/}
                <div className="w-full flex flex-col">
                    <div className="w-full font-medium pb-1 border-b border-b-black">Unread</div>
                </div>

                {/*=================================*/}
                {/*SUMMARIZE SECTION*/}
                {/*=================================*/}
                <div className="w-full flex flex-col">
                    <div className="w-full font-medium pb-1 border-b border-b-black">Summarize</div>
                </div>

                {/*=================================*/}
                {/*CHATS SECTION*/}
                {/*=================================*/}
                <div className="w-full flex flex-col">
                    <div className="w-full font-medium pb-1 border-b border-b-black">Chats</div>
                </div>
            </div>

            <ChatContent chat={chat}/>
        </div>
    )
}
