import Nullable from './Nullable.ts'

export default interface Tool {
    id: string
    projectId: string
    name: string
    jsonSchema: object
    description: Nullable<string>
}