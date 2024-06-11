import Message from './Message.ts'
import Nullable from './Nullable.ts'

export default interface jjChat {
    id: string
    name: string
    description: Nullable<string>
    project_id: string
    messages: Message[]
}