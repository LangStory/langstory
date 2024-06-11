import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import Chat from '@typing/Chat.ts'
import ApiCollectionResponse from '@typing/ApiCollectionResponse.ts'
import { URLS } from '@lib/constants.ts'

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
        <div className="w-1/2 h-3/4 m-auto mt-10 px-10 flex flex-col font-ibm uppercase">
            <div className="w-full font-medium pb-1 border-b border-b-black">Chats</div>
            <div className="w-full flex-grow mt-2 flex flex-col items-center space-y-2 overflow-y-auto">
                {chats.map((chat: Chat) => {
                    return (
                        <Link to={`/chats/${chat.id}`} key={chat.id} className="w-full flex p-2 uppercase rounded text-sm hover:bg-amber-500 hover:text-white">
                            <span className="flex flex-grow">{chat.name}</span> <span className="ml-2 text-2xs">{chat.description}</span>
                        </Link>
                    )
                })}
            </div>
        </div>
    )
}
