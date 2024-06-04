import { RefObject } from 'react'
import { format } from 'date-fns'
import { capitalize } from 'lodash'
import Nullable from 'types/Nullable.ts'
import Message, { MessageType } from 'types/Message.ts'
import { classNames } from 'lib/helpers.ts'

function getMessageClasses(type: MessageType): string {
    if (type === 'system_message') return 'bg-amber-400'
    if (type === 'assistant_message') return 'bg-fuchsia-600'
    if (type === 'tool_message') return 'bg-emerald-400'
    if (type === 'external_event') return 'bg-purple-500'
    return 'bg-sky-500'
}

interface Properties {
    message: Message
}

export default function MessageComponent({message}: Properties) {
    const classes: string = classNames('self-center w-full max-w-2xl flex flex-col px-4 py-3 rounded-md cursor-pointer font-ibm', getMessageClasses(message.type))
    return (
        <div key={message.id} className={classes}>
            <div className="w-full flex items-end space-x-2 text-sm text-slate-900">
                <div className="font-bold">{capitalize(message.role)}</div>
                <div className="text-xs text-slate-600">
                    {format(new Date(message.timestamp), 'h:mm a')}
                </div>
            </div>
            <div className="mt-2">
                {message.content}
            </div>
        </div>
    )
}
