import axios from 'axios'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { FormEvent, useEffect, useState } from 'react'
import { PlusIcon } from '@heroicons/react/24/outline'
import Chat from '@typing/Chat.ts'
import ApiCollectionResponse from '@typing/ApiCollectionResponse.ts'
import Nullable from '@typing/Nullable.ts'
import { URLS } from '@lib/constants.ts'
import { useAuth } from '@hooks/use-auth.tsx'
import Modal from '@components/core/Modal.tsx'

export default function ChatSidebar() {
    const navigate = useNavigate()
    const {signOut} = useAuth()
    const {id} = useParams()
    const [chats, setChats] = useState<Array<Chat>>([])
    const [showModal, setShowModal] = useState<boolean>(false)
    const [newChatName, setNewChatName] = useState<Nullable<string>>(null)

    useEffect(() => {
        async function fetchChats() {
            const {data} = await axios.get<ApiCollectionResponse<Chat>>(URLS.GET_CHATS())
            setChats(data.items)
        }

        fetchChats().then()
    }, [id])


    async function newChat(event: FormEvent) {
        event.preventDefault()
        setShowModal(false)
        try {
            const {data: projectData} = await axios(URLS.LIST_PROJECTS())
            const projectId = projectData.items[0].id
            const {data} = await axios.post<Chat>(URLS.CREATE_CHAT(), {
                name: newChatName,
                projectId
            })
            setNewChatName(null)
            navigate(`/chats/${data.id}`)
        } catch (e) {
            console.error(e)
            return
        }
    }

    return (
        <>
            {/*=================================*/}
            {/*MODAL*/}
            {/*=================================*/}
            <Modal displayed={showModal} setDisplayed={setShowModal}>
                <form onSubmit={newChat} className="p-6 bg-white space-y-4 rounded">
                    <div className="text-lg">New Chat Name</div>
                    <input type="text"
                           className="px-4 py-2 border border-gray-700 rounded"
                           value={newChatName || ''}
                           onChange={e => setNewChatName(e.target.value)}/>
                </form>
            </Modal>

            {/*=================================*/}
            {/*SIDEBAR*/}
            {/*=================================*/}
            <div className="w-1/5 h-full pt-10 px-8 flex flex-col items-center space-y-16 bg-gray-100">
                {/*=================================*/}
                {/*NEW CHAT BUTTON*/}
                {/*=================================*/}
                <button className="flex items-center" onClick={() => setShowModal(true)}>
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

                    <div className="h-80 mt-3 flex flex-col overflow-y-auto">
                        {chats.length > 0 && chats.reverse().map((chat: Chat) => {
                            return <Link to={`/chats/${chat.id}`} key={chat.id} className="w-full py-2 hover:text-sky-400">{chat.name}</Link>
                        })}
                    </div>
                </div>

                <div className="w-full self-end text-center text-sm cursor-pointer" onClick={signOut}>
                    Sign Out
                </div>
            </div>
        </>
    )
}