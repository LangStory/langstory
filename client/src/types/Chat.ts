import Message from 'types/Message.ts'

export default interface jjChat {
    id: string
    name: string
    description: string | null
    project_id: string
    messages: Message[]
}