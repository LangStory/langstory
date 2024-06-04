import Nullable from 'types/Nullable.ts'

export default interface Tool {
    id: string
    projectId: string
    name: string
    jsonSchema: string
    description: Nullable<string>
}