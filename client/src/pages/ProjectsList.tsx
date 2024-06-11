import { useEffect, useState } from 'react'
import Project from 'types/Project.ts'
import axios from 'axios'
import ApiCollectionResponse from 'types/ApiCollectionResponse.ts'
import { URLS } from 'lib/constants.ts'
import { Link } from 'react-router-dom'

export default function ProjectsList() {
    const [projects, setProjects] = useState<Array<Project>>([])

    useEffect(() => {
        async function fetchProjects() {
            const { data } = await axios.get<ApiCollectionResponse<Project>>(URLS.GET_PROJECTS())
            setProjects(data.items)
        }

        fetchProjects().then()
    }, [])

    return (
        <div className="w-1/2 m-auto mt-10 px-10 flex flex-col font-ibm uppercase h-screen">
            <div className="w-full font-medium pb-1 border-b border-b-black">Projects</div>
            <div className="w-full flex-grow mt-2 flex flex-col items-center space-y-2 overflow-y-auto">
                {projects.map((project: Project) => {
                    return (
                        <Link to={`/chats/${project.id}`} key={project.id} className="w-full flex p-2 uppercase rounded text-sm hover:bg-amber-500 hover:text-white">
                            <span className="flex flex-grow">{project.name}</span> <span className="ml-2 text-2xs">{project.description}</span>
                        </Link>
                    )
                })}
            </div>
        </div>
    )
}
