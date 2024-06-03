import { useEffect, useState } from 'react'
import Chat from 'types/Chat.ts'
import axios from 'axios'
import ApiCollectionResponse from 'types/ApiCollectionResponse.ts'
import { URLS } from 'lib/constants.ts'
import { Link } from 'react-router-dom'

export default function ChatsList() {
    const [chats, setChats] = useState<Array<Chat>>([])

    useEffect(() => {
        async function fetchChats() {
            const {data} = await axios.get<ApiCollectionResponse<Chat>>(URLS.GET_CHATS())
            setChats(data.items)
        }

        fetchChats().then()
    }, [])

    return (
        <div className="w-full flex flex-col">
            <div className="w-full font-medium pb-1 border-b border-b-black">Chats</div>
            {chats.length > 0 && chats.map((chat: Chat) => {
                return <Link to={`/chats/${chat.id}`} key={chat.id} className="w-full py-2">{chat.name}</Link>
            })}
        </div>
    )
}
