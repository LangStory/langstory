import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import Nullable from 'types/Nullable.ts'
import Tool from 'types/Tool.ts'
import { URLS } from 'lib/constants.ts'
import SchemaBuilder from 'components/SchemaBuilder.tsx'
import toast from 'react-hot-toast'

export default function ProjectToolComponent() {
    const {id: projectId} = useParams()
    const {id: toolId} = useParams()
    const [tool, setTool] = useState<Nullable<Tool>>(null)
    const [toolSchema, setToolSchema] = useState<Nullable<any>>(null)
    const [updatedSchema, setUpdatedSchema] = useState<Nullable<any>>(null)

    useEffect(() => {
        async function fetchChat() {
            if (toolId) {
                const {data} = await axios.get<Tool>(URLS.GET_TOOL(toolId))
                setTool(data)
                setToolSchema(data.jsonSchema)
            }
        }

        fetchChat().then()
    }, [toolId])

    async function save() {
        const tid = toolId!
        const name = updatedSchema.name
        const description = updatedSchema.description
        const jsonSchema = updatedSchema
        const {data} = await axios.post<{ id: string }>(URLS.UPDATE_TOOL(tid), {name, description, jsonSchema})
        if (data.id) {
            toast.success('Tool Updated')
        }
    }

    if (tool) return (
        <div className="w-full h-full py-10 px-8 flex flex-col justify-center items-center font-ibm space-y-4">
            <div className="relative w-full px-4 flex justify-center">
                <div className="font-bold uppercase text-xl">{tool.name}</div>
                <button
                    onClick={save}
                    className="absolute right-4 px-6 py-1 uppercase font-medium rounded bg-emerald-300 text-gray-700 hover:bg-emerald-400 hover:text-gray-800">
                    Save
                </button>
            </div>
            <SchemaBuilder initialSchema={toolSchema || {}} setUpdatedSchema={(o:any)=>setUpdatedSchema(o)}/>
        </div>
    )
    else return <></>
}
