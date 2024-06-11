import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import axios from 'axios'
import Tool from '@typing/Tool.ts'
import Project from '@typing/Project.ts'
import { URLS } from '@lib/constants.ts'

export default function ProjectToolsList() {
    const {id: projectId} = useParams()
    const [tools, setTools] = useState<Array<Tool>>([])

    useEffect(() => {
        async function fetchProject() {
            if (projectId) {
                const {data} = await axios.get<Project>(URLS.GET_PROJECT(projectId))
                setTools(data.tools)
            }
        }

        fetchProject().then()
    }, [projectId])

    return (
        <div className="w-full flex flex-col">
            <div className="w-full font-medium pl-10 pb-1 border-b border-b-black">ProjectTools</div>
            <div className="pl-10">
                {tools.map((tool: Tool) => {
                    return <Link to={`/projects/${projectId}/tools/${tool.id}`} key={tool.id} className="w-full py-2">{tool.name}</Link>
                })}
            </div>
        </div>
    )
}
