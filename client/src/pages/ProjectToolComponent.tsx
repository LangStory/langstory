import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import CodeMirror from '@uiw/react-codemirror'
import { json } from '@codemirror/lang-json'

import { JsonEditor } from 'json-edit-react'
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
        <div className="w-full h-screen mt-20 flex flex-col items-center font-ibm">
            {tool.name}
            <div className="w-full mt-10 flex justify-center space-x-10">
                <SchemaBuilder/>
                {/*<CodeMirror value={toolSchema || ''} width="250px" height="250px" extensions={[json()]} onChange={(value: string) => {*/}
                {/*    setToolSchema(value)*/}
                {/*}}/>*/}

                {/*<JsonEditor*/}
                {/*    data={() => {*/}
                {/*        try {*/}
                {/*            return JSON.parse(toolSchema || '')*/}
                {/*        } catch (e) {*/}
                {/*            return {}*/}
                {/*        }*/}
                {/*    }}*/}
                {/*    onUpdate={({newData}) => {*/}
                {/*        try {*/}
                {/*            setToolSchema(JSON.stringify(newData))*/}
                {/*        } catch (e) {*/}
                {/*            void (0)*/}
                {/*        }*/}
                {/*    }}/>*/}
            </div>
        </div>
    )
    else return <></>
}
