import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import axios from 'axios'
import Tool from 'types/Tool.ts'
import { URLS } from 'lib/constants.ts'
import Project from 'types/Project.ts'

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
            <div className="w-full font-medium pb-1 border-b border-b-black">ProjectTools</div>
            {tools.map((tool: Tool) => {
                return <Link to={`/projects/${projectId}/tools/${tool.id}`} key={tool.id} className="w-full py-2">{tool.name}</Link>
            })}
        </div>
    )
}
