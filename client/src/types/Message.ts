export type MessageRole = 'user' | 'system' | 'assistant' | 'tool'
export type MessageType = 'system_message' | 'user_message' | 'assistant_message' | 'tool_message' | 'external_event'

export default interface Message {
    id: string
    role: MessageRole
    type: MessageType
    content: string
    chat_id: string
}
