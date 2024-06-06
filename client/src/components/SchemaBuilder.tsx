import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import { PlusIcon } from '@heroicons/react/24/solid'
import { Square2StackIcon, TrashIcon } from '@heroicons/react/24/outline'
import { classNames } from 'lib/helpers.ts'

type FieldType = 'array' | 'boolean' | 'integer' | 'null' | 'number' | 'object' | 'string'

interface FieldObject {
    name: string;
    type: FieldType;
    parentIndex: number | null;
    index: number;
    description: string;
    required: boolean;
}

interface FieldProps {
    field: FieldObject;
    addField: (parentIndex: number | null, removeNested?: boolean) => void;
    updateField: (fieldIndex: number, name: string, type: FieldType, description: string, required: boolean) => void;
    deleteField: (fieldIndex: number) => void;
}

function Field({field, addField, updateField, deleteField}: FieldProps) {
    const [name, setName] = useState<string>(field.name)
    const [fieldType, setFieldType] = useState<FieldType>(field.type)
    const [description, setDescription] = useState<string>(field.description)
    const [required, setRequired] = useState<boolean>(field.required)

    useEffect(() => {
        setFieldType(field.type)
    }, [field.type])

    useEffect(() => {
        if (fieldType === 'object') {
            addField(field.index)
        } else {
            addField(field.index, true)
        }
    }, [fieldType])

    return (
        <div className="w-full my-6 py-3 flex flex-col items-start space-y-4 border-l-2 border-gray-300 pl-4">

            <div className="flex justify-between w-full items-center">
                <div className={classNames('flex flex-col space-y-1', fieldType === 'object' ? 'w-1/2' : 'w-full')}>
                    <label className="block text-sm font-medium text-gray-700">Type</label>
                    <select
                        value={fieldType}
                        className="p-2 border border-gray-300 rounded-md w-full"
                        onChange={e => {
                            const newType = e.target.value as FieldType
                            setFieldType(newType)
                            updateField(field.index, name, newType, description, required)
                        }}
                    >
                        <option value="string">string</option>
                        <option value="integer">integer</option>
                        <option value="number">number</option>
                        <option value="boolean">boolean</option>
                        <option value="null">null</option>
                        <option value="array">array</option>
                        <option value="object">object</option>
                    </select>
                </div>

                {fieldType === 'object' && (
                    <button
                        onClick={() => addField(field.index)}
                        className="self-end h-full w-fit ml-1 px-2 py-1 border border-gray-700 uppercase rounded flex items-center space-x-2 hover:bg-gray-700 hover:text-white"
                    >
                        <PlusIcon className="w-4 h-4"/>
                        <span className="text-sm font-medium">Add Nested Field</span>
                    </button>
                )}
            </div>

            <div className="flex flex-col space-y-1 w-full">
                <label className="block text-sm font-medium text-gray-700">Name</label>
                <input
                    type="text"
                    value={name}
                    className="p-2 border border-gray-300 rounded-md w-full"
                    onChange={e => {
                        setName(e.target.value)
                        updateField(field.index, e.target.value, fieldType, description, required)
                    }}
                />
            </div>

            <div className="flex flex-col space-y-1 w-full">
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <input
                    type="text"
                    value={description}
                    className="p-2 border border-gray-300 rounded-md w-full"
                    onChange={e => {
                        setDescription(e.target.value)
                        updateField(field.index, name, fieldType, e.target.value, required)
                    }}
                />
            </div>

            <div className="flex space-x-6 items-center w-full">
                <div className="self-start flex items-center space-x-6 w-full">
                    <label className="block text-sm font-medium text-gray-700">Required</label>
                    <input
                        type="checkbox"
                        checked={required}
                        className="border border-gray-300 rounded-md"
                        onChange={e => {
                            setRequired(e.target.checked)
                            updateField(field.index, name, fieldType, description, e.target.checked)
                        }}
                    />
                </div>
                <TrashIcon
                    className="self-end w-6 h-6 cursor-pointer"
                    onClick={() => deleteField(field.index)}
                />
            </div>
        </div>
    )
}

interface SchemaBuilderProps {
    schema: any;
}

export default function SchemaBuilder({schema}: SchemaBuilderProps) {
    const [fields, setFields] = useState<FieldObject[]>([])
    const [index, setIndex] = useState<number>(1)
    const [generatedSchema, setGeneratedSchema] = useState<object>({})
    const [functionName, setFunctionName] = useState<string>('')
    const [description, setDescription] = useState<string>('')
    const [topLevelRequired, setTopLevelRequired] = useState<string[]>([])

    useEffect(() => {
        if (schema) {
            const parseSchema = (schema: any, parentIndex: number | null) => {
                const entries = Object.entries(schema?.properties || {})
                entries.forEach(([name, prop]: [string, any], idx) => {
                    const newField: FieldObject = {
                        name,
                        type: prop.type as FieldType,
                        parentIndex,
                        index: index + idx,
                        description: prop.description || '',
                        required: (schema.required || []).includes(name),
                    }
                    setFields(prevFields => [...prevFields, newField])
                    if (prop.type === 'object' && prop.properties) {
                        setIndex(prevIndex => prevIndex + 1)
                        parseSchema(prop, index + idx)
                    }
                })
                setIndex(prevIndex => prevIndex + entries.length)
            }
            setFunctionName(schema.name || '')
            setDescription(schema.description || '')
            parseSchema(schema.parameters || {}, null)
        }
    }, [schema])

    const addField = (parentIndex: number | null, removeNested = false) => {
        if (removeNested) {
            setFields(fields.filter(field => field.parentIndex !== parentIndex))
        } else {
            setFields(prevFields => [
                ...prevFields,
                {
                    name: `field_${index}`,
                    type: 'string',
                    parentIndex,
                    index,
                    description: '',
                    required: false,
                },
            ])
            setIndex(index + 1)
        }
    }

    const deleteField = (fieldIndex: number) => {
        const deleteFieldAndNested = (index: number) => {
            setFields(prevFields => prevFields.filter(field => field.index !== index && field.parentIndex !== index))
        }
        deleteFieldAndNested(fieldIndex)
    }

    const updateField = (fieldIndex: number, name: string, type: FieldType, description: string, required: boolean) => {
        setFields(fields.map(field =>
            field.index === fieldIndex ? {...field, name, type, description, required} : field
        ))
    }

    const generateObject = () => {
        const buildObject = (parentIndex: number | null): any => {
            const result: any = {}
            const requiredFields: string[] = []

            fields
                .filter(field => field.parentIndex === parentIndex)
                .forEach(field => {
                    if (field.required) {
                        requiredFields.push(field.name)
                    }
                    if (field.type === 'object') {
                        const {properties, required} = buildObject(field.index)
                        result[field.name] = {
                            type: field.type,
                            description: field.description,
                            properties,
                        }
                        if (required.length > 0) {
                            result[field.name].required = required
                        }
                    } else {
                        result[field.name] = {
                            type: field.type,
                            description: field.description,
                        }
                    }
                })

            return {properties: result, required: requiredFields}
        }

        const {properties, required} = buildObject(null)

        const obj = {
            name: functionName,
            description: description,
            parameters: {
                type: 'object',
                properties,
                required: topLevelRequired.concat(required),
            },
        }

        setGeneratedSchema(obj)
    }

    useEffect(() => generateObject(), [fields, functionName, description, topLevelRequired])

    const renderFields = (parentIndex: number | null, depth: number = 0) => {
        const filteredFields = fields.filter(field => field.parentIndex === parentIndex)
        return filteredFields.map((field) => (
            <div key={field.index} style={{paddingLeft: depth * 30}}>
                <Field
                    field={field}
                    addField={addField}
                    updateField={updateField}
                    deleteField={deleteField}
                />
                {renderFields(field.index, depth + 1)}
            </div>
        ))
    }

    return (
        <div className="w-full h-screen flex flex-col overflow-hidden">
            <div className="w-full flex flex-grow justify-center space-x-10 overflow-hidden">
                {/*SCHEMA GUI*/}
                <div className="w-1/2 overflow-y-auto flex flex-col px-4">
                    {/*FUNCTION NAME*/}
                    <label className="block text-sm font-medium text-gray-700 mt-4">Function Name</label>
                    <input
                        type="text"
                        value={functionName}
                        onChange={e => setFunctionName(e.target.value)}
                        className="px-4 py-2 mb-4 border border-gray-300 rounded-md w-full"
                    />

                    {/*FUNCTION DESCRIPTION*/}
                    <label className="block text-sm font-medium text-gray-700">Function Description</label>
                    <input
                        type="text"
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                        className="px-4 py-2 mb-4 border border-gray-300 rounded-md w-full"
                    />

                    {/*ADD FIELD */}
                    <button
                        onClick={() => addField(null)}
                        className="w-fit ml-1 px-2 py-1 border border-gray-700 uppercase rounded flex items-center space-x-2 hover:bg-gray-700 hover:text-white"
                    >
                        <PlusIcon className="w-4 h-4"/>
                        <span className="text-sm font-medium">Add Field</span>
                    </button>

                    {renderFields(null)}
                </div>

                {/*GENERATED SCHEMA */}
                <div className="w-1/2 overflow-y-auto flex flex-col px-4">
                    <pre className="relative bg-gray-100 p-4 rounded mt-4 overflow-x-auto">
                        <Square2StackIcon
                            className="absolute top-5 right-5 w-6 h-6 cursor-pointer"
                            onClick={() => {
                                navigator.clipboard.writeText(JSON.stringify(generatedSchema, null, 2))
                                toast.success('Copied to clipboard')
                            }}
                        />
                        {JSON.stringify(generatedSchema, null, 2)}
                    </pre>
                </div>
            </div>
        </div>
    )
}
