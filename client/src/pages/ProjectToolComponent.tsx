import axios from 'axios'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import Tool from 'types/Tool.ts'
import { URLS } from 'lib/constants.ts'

export default function ProjectToolComponent() {
    const {id: toolId} = useParams()
    const [tool, setTool] = useState<Tool>()

    useEffect(() => {
        async function fetchChat() {
            if (toolId) {
                const {data} = await axios.get<Tool>(URLS.GET_TOOL(toolId))
                setTool(data)
            }
        }

        fetchChat().then()
    }, [toolId])

    return (
        <div className="w-full h-screen mt-20 flex flex-col items-center font-ibm">
            {JSON.stringify(tool)}
        </div>
    )
}
