import Message, { MessageType } from 'types/Message.ts'
import { classNames } from 'lib/helpers.ts'
import { RefObject } from 'react'
import Nullable from 'types/Nullable.ts'

function getMessageClasses(type: MessageType): string {
    if (type === 'system_message') return 'self-start bg-amber-400'
    if (type === 'assistant_message') return 'self-start bg-fuchsia-600'
    if (type === 'tool_message') return 'self-start bg-emerald-400'
    if (type === 'external_event') return 'self-start bg-purple-500'
    return 'self-end bg-sky-400'
}

interface Properties {
    message: Message
    ref?: Nullable<RefObject<HTMLDivElement>>
}

export default function MessageComponent({message, ref = null}: Properties) {
    const classes: string = classNames('w-fit px-4 py-3 rounded-md cursor-pointer font-ibm', getMessageClasses(message.type))
    return (
        <div key={message.id} className={classes} ref={ref}>
            {message.content}
        </div>
    )
}
