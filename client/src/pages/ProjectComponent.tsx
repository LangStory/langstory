import axios from 'axios'
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import Project from 'types/Project.ts'
import Nullable from 'types/Nullable.ts'
import { URLS } from 'lib/constants.ts'
import Tool from 'types/Tool.ts'

export default function ProjectComponent() {
    const {id: projectId} = useParams()
    const [project, setProject] = useState<Nullable<Project>>()

    useEffect(() => {
        async function fetchProject() {
            if (projectId) {
                const {data} = await axios.get<Project>(URLS.GET_PROJECT(projectId))
                setProject(data)
            }
        }

        fetchProject().then()
    }, [projectId])

    if (project) return (
        <div className="w-full h-screen mt-20 flex flex-col items-center font-ibm">
            <div className="text-xl">Project: {project.name} </div>
            <div className="mt-10 text-lg">Tools</div>
            <div className="w-1/2 flex flex-col items-center">
                {project.tools.map((tool: Tool) => {
                    return <Link to={`/projects/${projectId}/tools/${tool.id}`} key={tool.id} className="w-full py-2">{tool.name}</Link>
                })}
            </div>
        </div>
    )
    else return <></>
}
