export type MessageType = 'user' | 'message' | 'assistant' | 'tool'

export default interface Message {
    id: string
    role: MessageType
    content: string
    chat_id: string
}