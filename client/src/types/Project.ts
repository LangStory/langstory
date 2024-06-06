import Nullable from 'types/Nullable.ts'
import Tool from 'types/Tool.ts'

export default interface Project {
    id: string
    name: string
    description: Nullable<string>
    organizationId: Nullable<string>
    avatarUrl: Nullable<string>
    tools: Array<Tool>
}