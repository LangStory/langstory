import { ReactNode, useState } from 'react'
import { PlusIcon } from '@heroicons/react/24/solid'

type FieldType = 'string' | 'number' | 'boolean' | 'array' | 'object'

interface FieldProps {
    type: FieldType
    index: number
    addField: () => void
    updateName: (name: string) => void
    updateType: (type: string) => void
}

interface FieldObject {
    name: string
    type: string
    field: ReactNode
}

function Field({type, index, addField, updateName, updateType}: FieldProps) {
    const [name, setName] = useState<string>(`Input ${index}`)
    const [fieldType, setFieldType] = useState<string>(type)
    return (
        <div className="w-full flex flex-col items-center space-y-4 font-ibm">
            <div className="flex flex-col space-y-1">
                <label className="text-sm">Type</label>
                <input type="text"
                       value={fieldType}
                       className="px-4 py-2 border border-gray-300 rounded-lg text-center"
                       onChange={e => {
                           setFieldType(e.target.value)
                           updateType(e.target.value)
                       }}/>
            </div>

            <div className="flex flex-col space-y-1">
                <label className="text-sm">Name</label>
                <input type="text"
                       value={name}
                       className="px-4 py-2 border border-gray-300 rounded-lg text-center"
                       onChange={e => {
                           setName(e.target.value)
                           updateName(e.target.value)
                       }}/>
            </div>
            <button onClick={addField}><PlusIcon className="w-6 h-6"/></button>
        </div>
    )
}

export default function SchemaBuilder() {
    const [schema, setSchema] = useState<string>('')
    const [index, setIndex] = useState<number>(1)
    const [fields, setFields] = useState<Array<FieldObject>>([
        {
            name: `Input ${index}`,
            type: 'string',
            field: <Field
                type="string"
                index={index}
                addField={addField}
                updateName={(newName: string) => {
                    const myField = fields.find(field => field.name === `Input ${index}`)
                    if (myField) {
                        myField.name = newName
                        setFields([...fields])
                    }
                }}
                updateType={(newType: string) => {
                    const myField = fields.find(field => field.name === `Input ${index}`)
                    if (myField) {
                        myField.type = newType
                        setFields([...fields])
                    }
                }}
            />
        }
    ])

    function addField() {
        setIndex(index + 1)
        setFields([...fields,
            {
                name: `Input ${index}`,
                type: 'string',
                field: <Field
                    type="string"
                    index={index}
                    addField={addField}
                    updateName={(newName: string) => {
                        const myField = fields.find(field => field.name === `Input ${index}`)
                        if (myField) {
                            myField.name = newName
                            setFields([...fields])
                        }
                    }}
                    updateType={(newType: string) => {
                        const myField = fields.find(field => field.name === `Input ${index}`)
                        if (myField) {
                            myField.type = newType
                            setFields([...fields])
                        }
                    }}
                />
            }
        ])
    }

    return (
        <div className="w-full flex flex-col justify-center items-center">
            {fields.map((field: FieldObject) => {
                return field.field
            })}
        </div>
    )
}