import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import Nullable from 'types/Nullable.ts'
import Tool from 'types/Tool.ts'
import { URLS } from 'lib/constants.ts'
import SchemaBuilder from 'components/SchemaBuilder.tsx'

export default function ProjectToolComponent() {
    const {id: toolId} = useParams()
    const [tool, setTool] = useState<Nullable<Tool>>(null)
    const [toolSchema, setToolSchema] = useState<Nullable<string>>(null)

    useEffect(() => {
        async function fetchChat() {
            if (toolId) {
                const {data} = await axios.get<Tool>(URLS.GET_TOOL(toolId))
                setTool(data)
                setToolSchema(JSON.stringify(data.jsonSchema))
            }
        }

        fetchChat().then()
    }, [toolId])

    if (tool) return (
        <div className="w-full h-full py-10 flex flex-col justify-center items-center font-ibm space-y-4">
            <div className="font-bold uppercase text-xl">{tool.name}</div>
            <SchemaBuilder schema={{}}/>
        </div>
    )
    else return <></>
}
