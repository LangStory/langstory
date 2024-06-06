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
            const {data} = await axios.get<ApiCollectionResponse<Project>>(URLS.GET_PROJECTS())
            setProjects(data.items)
        }

        fetchProjects().then()
    }, [])

    return (
        <div className="w-full flex flex-col">
            <div className="w-full font-medium pb-1 border-b border-b-black">Projects</div>
            {projects.length > 0 && projects.map((project: Project) => {
                return <Link to={`/projects/${project.id}`} key={project.id} className="w-full py-2">{project.name}</Link>
            })}
        </div>
    )
}
