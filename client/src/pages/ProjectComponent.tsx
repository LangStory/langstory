import { useEffect, useState } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Nullable from 'types/Nullable.ts'
import Project from 'types/Project.ts'
import Tool from 'types/Tool.ts'
import { URLS } from 'lib/constants.ts'
import Modal from 'components/core/Modal.tsx'

export default function ProjectComponent() {
    const {id: projectId} = useParams()
    const navigate = useNavigate()
    const [project, setProject] = useState<Nullable<Project>>()
    const [showModal, setShowModal] = useState<boolean>(false)
    const [functionName, setFunctionName] = useState<string>('')
    const [functionDescription, setFunctionDescription] = useState<string>('')

    useEffect(() => {
        async function fetchProject() {
            if (projectId) {
                const {data} = await axios.get<Project>(URLS.GET_PROJECT(projectId))
                setProject(data)
            }
        }

        fetchProject().then()
    }, [projectId])

    async function createNewTool() {
        const json_schema = {
            'name': functionName,
            'description': functionDescription,
            'parameters': {
                'type': 'object',
                'properties': {
                    'param_1': {
                        'type': 'string',
                        'description': 'this is the first parameter'
                    }
                },
                'required': [
                    'param_1'
                ]
            }
        }

        const {data} = await axios.post<{ id: string }>(URLS.CREATE_TOOL(), {
            name: functionName,
            description: functionDescription,
            project_id: projectId,
            json_schema
        })
        if (data.id) {
            navigate(`/projects/${projectId}/tools/${data.id}`)
        }
    }

    if (project) return (
        <>
            <Modal displayed={showModal} setDisplayed={setShowModal}>
                <div className="w-full py-8 px-10 bg-white rounded space-y-6">
                    <div className="text-sm font-bold uppercase border-b border-b-gray-700">New Tool</div>
                    <div className="flex flex-col justify-start space-y-1">
                        <label className="block text-sm font-medium text-gray-700">Function Name</label>
                        <input
                            type="text"
                            value={functionName}
                            onChange={e => setFunctionName(e.target.value)}
                            className="px-4 py-2 mb-4 border border-gray-300 rounded-md w-full"
                        />
                    </div>

                    <div className="flex flex-col space-y-1">
                        <label className="block text-sm font-medium text-gray-700">Function Description</label>
                        <input
                            type="text"
                            value={functionDescription}
                            onChange={e => setFunctionDescription(e.target.value)}
                            className="px-4 py-2 mb-4 border border-gray-300 rounded-md w-full"
                        />
                    </div>

                    <div className="flex justify-center">
                        <button
                            onClick={createNewTool}
                            className="w-full px-4 py-2 rounded bg-emerald-300 hover:bg-emerald-400 uppercase font-medium text-sm">
                            Create
                        </button>
                    </div>
                </div>
            </Modal>

            <div className="w-1/2 m-auto h-screen mt-10 px-10 flex flex-col font-ibm uppercase">
                <div className="text-xs">Project <span className="ml-2 text-xl font-medium">{project.name}</span></div>
                <div className="w-full mt-10 pb-1 flex items-center text-sm font-medium border-b border-b-gray-700">
                    <div className="flex flex-grow">
                        Tools
                    </div>
                    <button className="self-end rounded px-4 py-1 bg-emerald-300 hover:bg-emerald-400" onClick={() => setShowModal(true)}>
                        NEW TOOL
                    </button>
                </div>
                <div className="w-full mt-2 flex flex-col items-center space-y-2">
                    {project.tools.map((tool: Tool) => {
                        return <Link to={`/projects/${projectId}/tools/${tool.id}`} key={tool.id} className="w-full p-2 uppercase rounded text-sm hover:bg-amber-500 hover:text-white">{tool.name}</Link>
                    })}
                </div>
            </div>
        </>
    )
    else return <></>
}
