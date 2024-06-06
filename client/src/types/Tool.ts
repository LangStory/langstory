import Nullable from 'types/Nullable.ts'

export default interface Tool {
    id: string
    projectId: string
    name: string
    jsonSchema: object
    description: Nullable<string>
}