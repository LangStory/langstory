import { useState, useEffect } from 'react'
import { PlusIcon } from '@heroicons/react/24/solid'
import Optional from 'types/Optional.ts'

type FieldType = 'string' | 'number' | 'boolean' | 'array' | 'object';

interface FieldObject {
    name: string;
    type: FieldType;
    parentIndex: number | null;
    index: number;
    nested?: Array<FieldObject>
}

interface FieldProps {
    field: FieldObject;
    addField: (parentIndex: number | null) => void;
    updateField: (fieldIndex: number, name: string, type: FieldType) => void;
}

function Field({field, addField, updateField}: FieldProps) {
    const [name, setName] = useState<string>(field.name)
    const [fieldType, setFieldType] = useState<FieldType>(field.type)

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
                        updateField(field.index, name, newType)
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
                        updateField(field.index, e.target.value, fieldType)
                    }}
                />
            </div>

            <button onClick={() => addField(field.index)} className="flex items-center">
                <PlusIcon className="w-6 h-6 mr-2"/>
                Add Nested Field
            </button>
        </div>
    )
}

function GeneratedSchema({schema}: { schema: object }) {
    return (
        <div className="w-full mt-8">
            <h3 className="text-lg font-semibold">Generated JSON Schema:</h3>
            <pre className="bg-gray-100 p-4 rounded overflow-x-auto">{JSON.stringify(schema, null, 2)}</pre>
        </div>
    )
}

export default function SchemaBuilder() {
    const [fields, setFields] = useState<FieldObject[]>([
        {name: 'Field 1', type: 'string', parentIndex: null, index: 1},
    ])
    const [index, setIndex] = useState<number>(2)
    const [schema, setSchema] = useState<object>({})

    const addField = (parentIndex: number | null) => {
        const newField: FieldObject = {
            name: `Field ${index}`,
            type: 'string',
            parentIndex,
            index,
            nested: [],
        }

        if (parentIndex !== null) {
            const parentField: Optional<FieldObject> = fields.find(field => field.index === parentIndex)
            if (parentField) {
                parentField.nested = parentField.nested || []
                parentField.nested.push(newField)
                const otherFields = fields.filter(field => field.index !== parentIndex)
                setFields([...otherFields, parentField])
            }
        } else {
            setFields([...fields, newField])
        }

        setIndex(index + 1)
    }

    const updateField = (fieldIndex: number, name: string, type: FieldType) => {
        const updateNestedFields = (fields: FieldObject[]): FieldObject[] => {
            return fields.map(field => {
                if (field.index === fieldIndex) {
                    return {...field, name, type}
                } else if (field.nested && field.nested.length > 0) {
                    return {...field, nested: updateNestedFields(field.nested)}
                }
                return field
            })
        }

        setFields(updateNestedFields(fields))
    }

    const generateSchema = () => {
        const buildSchema = (fields: FieldObject[]): any => {
            const result: any = {}
            fields.forEach(field => {
                if (field.type === 'object' && field.nested) {
                    result[field.name] = {
                        type: field.type,
                        properties: buildSchema(field.nested),
                    }
                } else {
                    result[field.name] = {type: field.type}
                }
            })
            return result
        }

        const rootFields = fields.filter(field => field.parentIndex === null)
        const schema = {type: 'object', properties: buildSchema(rootFields)}
        setSchema(schema)
    }

    useEffect(() => {
        generateSchema()
    }, [fields])

    const renderFields = (parentIndex: number | null, depth: number = 0) => {
        return fields
            .filter(field => field.parentIndex === parentIndex)
            .map(field => (
                <div key={field.index} style={{paddingLeft: depth * 20}}>
                    <Field
                        field={field}
                        addField={addField}
                        updateField={updateField}
                    />
                    {field.nested && renderFields(field.index, depth + 1)}
                </div>
            ))
    }

    return (
        <div className="w-full flex flex-col justify-center items-center">
            <div className="w-full flex justify-center">
                <button onClick={() => addField(null)} className="flex items-center mb-4">
                    <PlusIcon className="w-6 h-6 mr-2"/>
                    Add Field at Root Level
                </button>
            </div>
            {renderFields(null)}
            <GeneratedSchema schema={schema}/>
        </div>
    )
}
