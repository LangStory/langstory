import { useState, useEffect } from 'react'
import { PlusIcon } from '@heroicons/react/24/solid'

type FieldType = 'string' | 'number' | 'boolean' | 'array' | 'object';

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
    addNestedFieldButton: boolean;
}

const Field: React.FC<FieldProps> = ({field, addField, updateField, addNestedFieldButton}) => {
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
        <div className="w-full flex flex-col items-start space-y-4 border-l-2 border-gray-300 pl-4">
            <div className="flex flex-col space-y-1 w-full">
                <label className="text-sm">Type</label>
                <select
                    value={fieldType}
                    className="px-4 py-2 border border-gray-300 rounded-lg w-full"
                    onChange={e => {
                        const newType = e.target.value as FieldType
                        setFieldType(newType)
                        updateField(field.index, name, newType, description, required)
                    }}
                >
                    <option value="string">String</option>
                    <option value="number">Number</option>
                    <option value="boolean">Boolean</option>
                    <option value="array">Array</option>
                    <option value="object">Object</option>
                </select>
            </div>

            <div className="flex flex-col space-y-1 w-full">
                <label className="text-sm">Name</label>
                <input
                    type="text"
                    value={name}
                    className="px-4 py-2 border border-gray-300 rounded-lg w-full"
                    onChange={e => {
                        setName(e.target.value)
                        updateField(field.index, e.target.value, fieldType, description, required)
                    }}
                />
            </div>

            <div className="flex flex-col space-y-1 w-full">
                <label className="text-sm">Description</label>
                <input
                    type="text"
                    value={description}
                    className="px-4 py-2 border border-gray-300 rounded-lg w-full"
                    onChange={e => {
                        setDescription(e.target.value)
                        updateField(field.index, name, fieldType, e.target.value, required)
                    }}
                />
            </div>

            <div className="flex flex-col space-y-1 w-full">
                <label className="text-sm">Required</label>
                <input
                    type="checkbox"
                    checked={required}
                    className="px-4 py-2 border border-gray-300 rounded-lg"
                    onChange={e => {
                        setRequired(e.target.checked)
                        updateField(field.index, name, fieldType, description, e.target.checked)
                    }}
                />
            </div>

            {fieldType === 'object' && addNestedFieldButton && (
                <button onClick={() => addField(field.index)} className="flex items-center">
                    <PlusIcon className="w-6 h-6 mr-2"/>
                    Add Nested Field
                </button>
            )}
        </div>
    )
}

const GeneratedObject: React.FC<{ obj: object }> = ({obj}) => {
    return (
        <div className="w-1/2">
            <pre className="bg-gray-100 p-4 rounded overflow-x-auto">{JSON.stringify(obj, null, 2)}</pre>
        </div>
    )
}

export default function SchemaBuilder() {
    const [fields, setFields] = useState<FieldObject[]>([
        {name: 'field_1', type: 'string', parentIndex: null, index: 1, description: '', required: false},
    ])
    const [index, setIndex] = useState<number>(2)
    const [generatedObject, setGeneratedObject] = useState<object>({})
    const [functionName, setFunctionName] = useState<string>('')
    const [description, setDescription] = useState<string>('')
    const [topLevelRequired, setTopLevelRequired] = useState<string[]>([])

    const addField = (parentIndex: number | null, removeNested = false) => {
        if (removeNested) {
            setFields(fields.filter(field => field.parentIndex !== parentIndex))
        } else {
            setFields([
                ...fields,
                {
                    name: `field_${index}`,
                    type: 'string',
                    parentIndex,
                    index,
                    description: '',
                    required: false
                },
            ])
            setIndex(index + 1)
        }
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
                            description: field.description
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
                required: topLevelRequired.concat(required)
            }
        }

        setGeneratedObject(obj)
    }

    useEffect(() => generateObject(), [fields, functionName, description, topLevelRequired])

    const renderFields = (parentIndex: number | null, depth: number = 0) => {
        return fields
            .filter(field => field.parentIndex === parentIndex)
            .map((field, idx, arr) => (
                <div key={field.index} style={{paddingLeft: depth * 20}}>
                    <Field
                        field={field}
                        addField={addField}
                        updateField={updateField}
                        addNestedFieldButton={idx === arr.length - 1}
                    />
                    {renderFields(field.index, depth + 1)}
                </div>
            ))
    }

    return (
        <div className="w-full flex flex-col justify-center items-center">
            <div className="w-full px-20 flex justify-center space-x-10 overflow-y-auto">
                <div className="w-1/2">
                    <label className="block text-sm font-medium text-gray-700">Function Name</label>
                    <input
                        type="text"
                        value={functionName}
                        onChange={e => setFunctionName(e.target.value)}
                        className="px-4 py-2 mb-4 border border-gray-300 rounded-lg w-full"
                    />
                    <label className="block text-sm font-medium text-gray-700">Description</label>
                    <input
                        type="text"
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                        className="px-4 py-2 mb-4 border border-gray-300 rounded-lg w-full"
                    />
                    <label className="block text-sm font-medium text-gray-700">Required Top Level Fields (comma-separated)</label>
                    <input
                        type="text"
                        value={topLevelRequired.join(', ')}
                        onChange={e => setTopLevelRequired(e.target.value.split(',').map(s => s.trim()))}
                        className="px-4 py-2 mb-4 border border-gray-300 rounded-lg w-full"
                    />
                    <button onClick={() => addField(null)} className="flex items-center mb-4">
                        <PlusIcon className="w-6 h-6 mr-2"/>
                        Add Field
                    </button>
                    {renderFields(null)}
                </div>

                <GeneratedObject obj={generatedObject}/>
            </div>
        </div>
    )
}
