import Message from 'types/Message.ts'
import Nullable from 'types/Nullable.ts'

export default interface jjChat {
    id: string
    name: string
    description: Nullable<string>
    project_id: string
    messages: Message[]
}