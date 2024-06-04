import axios from 'axios'
import Chat from 'types/Chat.ts'
import { URLS } from 'lib/constants.ts'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import ChatContent from 'components/ChatContent.tsx'
import Nullable from 'types/Nullable.ts'
import ChatSidebar from 'components/ChatSidebar.tsx'
import Modal from 'components/core/Modal.tsx'

export default function ChatComponent() {
    const {id: chatId} = useParams()
    const [chat, setChat] = useState<Nullable<Chat>>()

    useEffect(() => {
        async function fetchChat() {
            if (chatId) {
                const {data} = await axios.get<Chat>(URLS.GET_CHAT(chatId))
                setChat(data)
            }
        }

        fetchChat().then()
    }, [chatId])

    return (
        <div className="w-full h-screen flex font-ibm">
            <ChatSidebar/>
            <ChatContent chat={chat}/>
        </div>
    )
}
